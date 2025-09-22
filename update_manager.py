#!/usr/bin/env python3

"""
Auto Update System
Checks for new versions and handles automatic updates
"""

import json
import os
import sys
import requests
import zipfile
import tempfile
import shutil
import subprocess
from datetime import datetime
from packaging import version as pkg_version
from PySide6.QtCore import QThread, Signal, QObject, QTimer, Qt
from PySide6.QtWidgets import QMessageBox, QProgressDialog, QApplication
from PySide6.QtGui import QIcon

class UpdateChecker(QThread):
    """Thread for checking updates without blocking UI"""
    update_available = Signal(dict)
    update_not_available = Signal()
    error_occurred = Signal(str)
    
    def __init__(self, current_version, github_repo="bibekchandsah/pc-checker"):
        super().__init__()
        self.current_version = current_version
        self.github_repo = github_repo
        self.github_api_url = f"https://api.github.com/repos/{github_repo}/releases/latest"
        
    def run(self):
        """Check for updates in background thread"""
        try:
            # Test internet connectivity first with multiple reliable endpoints
            connection_available = self._test_internet_connection()
            if not connection_available:
                self.error_occurred.emit("No internet connection")
                return
            
            # Get latest release info from GitHub
            try:
                response = requests.get(self.github_api_url, timeout=10)
                if response.status_code == 404:
                    self.error_occurred.emit("Repository not found - please check the repository URL")
                    return
                elif response.status_code == 403:
                    self.error_occurred.emit("API rate limit exceeded - please try again later")
                    return
                elif response.status_code != 200:
                    self.error_occurred.emit(f"GitHub API error: HTTP {response.status_code}")
                    return
            except requests.exceptions.ConnectionError:
                self.error_occurred.emit("No internet connection")
                return
            except requests.exceptions.Timeout:
                self.error_occurred.emit("GitHub API timeout - please try again")
                return
            except requests.exceptions.RequestException as e:
                self.error_occurred.emit(f"Failed to connect to GitHub: {str(e)}")
                return
            
            release_data = response.json()
            latest_version = release_data.get('tag_name', '').lstrip('v')
            
            if not latest_version:
                self.error_occurred.emit("Invalid version information from GitHub")
                return
            
            # Compare versions
            try:
                if pkg_version.parse(latest_version) > pkg_version.parse(self.current_version):
                    update_info = {
                        'version': latest_version,
                        'name': release_data.get('name', f'Version {latest_version}'),
                        'body': release_data.get('body', 'No release notes available'),
                        'published_at': release_data.get('published_at', ''),
                        'download_url': self._get_download_url(release_data),
                        'size': self._get_download_size(release_data)
                    }
                    self.update_available.emit(update_info)
                else:
                    self.update_not_available.emit()
            except Exception as e:
                self.error_occurred.emit(f"Version comparison error: {str(e)}")
                
        except Exception as e:
            self.error_occurred.emit(f"Unexpected error: {str(e)}")
    
    def _test_internet_connection(self):
        """Test internet connectivity using multiple reliable endpoints"""
        test_urls = [
            "https://www.google.com",
            "https://www.cloudflare.com", 
            "https://httpbin.org/get",
            "https://api.github.com"
        ]
        
        for url in test_urls:
            try:
                response = requests.get(url, timeout=3)
                if response.status_code == 200:
                    return True
            except requests.exceptions.RequestException:
                continue
        
        return False
    
    def _get_download_url(self, release_data):
        """Get the download URL for the release"""
        assets = release_data.get('assets', [])
        
        # Look for a Windows executable or zip file
        for asset in assets:
            name = asset.get('name', '').lower()
            if any(ext in name for ext in ['.exe', '.zip', 'windows', 'win']):
                return asset.get('browser_download_url')
        
        # Fallback to source code zip
        return release_data.get('zipball_url')
    
    def _get_download_size(self, release_data):
        """Get the download size"""
        assets = release_data.get('assets', [])
        for asset in assets:
            name = asset.get('name', '').lower()
            if any(ext in name for ext in ['.exe', '.zip', 'windows', 'win']):
                return asset.get('size', 0)
        return 0

class UpdateDownloader(QThread):
    """Thread for downloading updates"""
    download_progress = Signal(int, int)  # current, total
    download_completed = Signal(str)  # file_path
    download_failed = Signal(str)  # error_message
    
    def __init__(self, download_url, file_name):
        super().__init__()
        self.download_url = download_url
        self.file_name = file_name
        self.download_path = os.path.join(tempfile.gettempdir(), file_name)
    
    def run(self):
        """Download the update file"""
        try:
            response = requests.get(self.download_url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0
            
            with open(self.download_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk)
                        self.download_progress.emit(downloaded_size, total_size)
            
            self.download_completed.emit(self.download_path)
            
        except Exception as e:
            self.download_failed.emit(str(e))

class UpdateManager(QObject):
    """Main update manager class"""
    
    def __init__(self, parent, current_version):
        super().__init__(parent)
        self.parent = parent
        self.current_version = current_version
        self.update_checker = None
        self.update_downloader = None
        self.progress_dialog = None
        
    def check_for_updates(self, show_no_update_message=False):
        """Start checking for updates"""
        if self.update_checker and self.update_checker.isRunning():
            return
        
        self.show_no_update_message = show_no_update_message
        self.update_checker = UpdateChecker(self.current_version)
        self.update_checker.update_available.connect(self._on_update_available)
        self.update_checker.update_not_available.connect(self._on_no_update)
        self.update_checker.error_occurred.connect(self._on_update_error)
        self.update_checker.start()
        
        # Show checking message
        if hasattr(self.parent, 'status_label'):
            self.parent.status_label.setText("Checking for updates...")
    
    def _on_update_available(self, update_info):
        """Handle when update is available"""
        if hasattr(self.parent, 'status_label'):
            self.parent.status_label.setText(f"Update available: v{update_info['version']}")
        
        # Create update notification dialog
        msg = QMessageBox(self.parent)
        msg.setWindowTitle("Update Available")
        msg.setIcon(QMessageBox.Icon.Information)
        
        # Set window icon if available
        icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        if os.path.exists(icon_path):
            msg.setWindowIcon(QIcon(icon_path))
        
        # Format the message
        published_date = ""
        if update_info['published_at']:
            try:
                pub_date = datetime.fromisoformat(update_info['published_at'].replace('Z', '+00:00'))
                published_date = pub_date.strftime("%B %d, %Y")
            except:
                published_date = update_info['published_at']
        
        size_info = ""
        if update_info['size'] > 0:
            size_mb = update_info['size'] / (1024 * 1024)
            size_info = f" ({size_mb:.1f} MB)"
        
        message = f"""A new version of Laptop testing Program is available!

Current Version: {self.current_version}
Latest Version: {update_info['version']}
{f"Released: {published_date}" if published_date else ""}
{f"Download Size: {size_info}" if size_info else ""}

What's New:
{update_info['body'][:500]}{"..." if len(update_info['body']) > 500 else ""}

Would you like to download and install the update now?"""
        
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
        msg.setDefaultButton(QMessageBox.StandardButton.Yes)
        
        # Customize button text
        yes_button = msg.button(QMessageBox.StandardButton.Yes)
        no_button = msg.button(QMessageBox.StandardButton.No)
        cancel_button = msg.button(QMessageBox.StandardButton.Cancel)
        
        yes_button.setText("Download Now")
        no_button.setText("Remind Later")
        cancel_button.setText("Skip This Version")
        
        result = msg.exec()
        
        if result == QMessageBox.StandardButton.Yes:
            self._download_update(update_info)
        elif result == QMessageBox.StandardButton.No:
            # Set reminder for next startup
            self._set_update_reminder(update_info)
        # Cancel = do nothing
    
    def _on_no_update(self):
        """Handle when no update is available"""
        if hasattr(self.parent, 'status_label'):
            self.parent.status_label.setText("You have the latest version")
        
        if self.show_no_update_message:
            msg = QMessageBox(self.parent)
            msg.setWindowTitle("No Updates")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setText(f"You are already running the latest version ({self.current_version})")
            
            # Set window icon if available
            icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
            if os.path.exists(icon_path):
                msg.setWindowIcon(QIcon(icon_path))
            
            msg.exec()
    
    def _on_update_error(self, error_message):
        """Handle update check errors"""
        if hasattr(self.parent, 'status_label'):
            # Set appropriate status based on error type
            if "No internet connection" in error_message:
                self.parent.status_label.setText("No internet connection")
            elif "timeout" in error_message.lower():
                self.parent.status_label.setText("Connection timeout")
            elif "rate limit" in error_message.lower():
                self.parent.status_label.setText("API rate limit exceeded")
            else:
                self.parent.status_label.setText("Update check failed")
        
        if self.show_no_update_message:
            msg = QMessageBox(self.parent)
            msg.setWindowTitle("Update Check Failed")
            msg.setIcon(QMessageBox.Icon.Warning)
            
            # Customize message based on error type
            if "No internet connection" in error_message:
                msg.setText("Unable to check for updates.\n\nPlease check your internet connection and try again.")
            elif "timeout" in error_message.lower():
                msg.setText("Update check timed out.\n\nPlease check your internet connection and try again.")
            elif "rate limit" in error_message.lower():
                msg.setText("GitHub API rate limit exceeded.\n\nPlease try again in a few minutes.")
            elif "Repository not found" in error_message:
                msg.setText("Repository not found.\n\nThe update source may have moved or be unavailable.")
            else:
                msg.setText(f"Failed to check for updates:\n\n{error_message}")
            
            # Set window icon if available
            icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
            if os.path.exists(icon_path):
                msg.setWindowIcon(QIcon(icon_path))
            
            msg.exec()
    
    def _download_update(self, update_info):
        """Start downloading the update"""
        if not update_info['download_url']:
            QMessageBox.warning(self.parent, "Download Error", "No download URL available for this update.")
            return
        
        # Determine file name
        file_name = f"pc-checker-{update_info['version']}.zip"
        if update_info['download_url'].endswith('.exe'):
            file_name = f"pc-checker-{update_info['version']}.exe"
        
        # Create progress dialog
        self.progress_dialog = QProgressDialog("Downloading update...", "Cancel", 0, 100, self.parent)
        self.progress_dialog.setWindowTitle("Downloading Update")
        self.progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        
        # Set window icon if available
        icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        if os.path.exists(icon_path):
            self.progress_dialog.setWindowIcon(QIcon(icon_path))
        
        # Start download
        self.update_downloader = UpdateDownloader(update_info['download_url'], file_name)
        self.update_downloader.download_progress.connect(self._on_download_progress)
        self.update_downloader.download_completed.connect(self._on_download_completed)
        self.update_downloader.download_failed.connect(self._on_download_failed)
        self.progress_dialog.canceled.connect(self._cancel_download)
        
        self.update_downloader.start()
        self.progress_dialog.show()
    
    def _on_download_progress(self, current, total):
        """Update download progress"""
        if self.progress_dialog and total > 0:
            progress = int((current / total) * 100)
            self.progress_dialog.setValue(progress)
            self.progress_dialog.setLabelText(f"Downloading update... {progress}% ({current/1024/1024:.1f}/{total/1024/1024:.1f} MB)")
    
    def _on_download_completed(self, file_path):
        """Handle download completion"""
        if self.progress_dialog:
            self.progress_dialog.close()
        
        # Show installation dialog
        msg = QMessageBox(self.parent)
        msg.setWindowTitle("Download Completed")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText(f"Update downloaded successfully!\n\nFile saved to: {file_path}\n\nWould you like to install it now?")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.Yes)
        
        # Set window icon if available
        icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        if os.path.exists(icon_path):
            msg.setWindowIcon(QIcon(icon_path))
        
        if msg.exec() == QMessageBox.StandardButton.Yes:
            self._install_update(file_path)
    
    def _on_download_failed(self, error_message):
        """Handle download failure"""
        if self.progress_dialog:
            self.progress_dialog.close()
        
        QMessageBox.critical(self.parent, "Download Failed", f"Failed to download update:\n\n{error_message}")
    
    def _cancel_download(self):
        """Cancel the download"""
        if self.update_downloader:
            self.update_downloader.terminate()
            self.update_downloader.wait()
    
    def _install_update(self, file_path):
        """Install the downloaded update"""
        try:
            if file_path.endswith('.exe'):
                # Direct executable installation
                os.startfile(file_path)
                QApplication.quit()
            elif file_path.endswith('.zip'):
                # Extract and install
                self._install_from_zip(file_path)
            else:
                # Open file location for manual installation
                os.startfile(os.path.dirname(file_path))
                
                msg = QMessageBox(self.parent)
                msg.setWindowTitle("Manual Installation")
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setText(f"Please manually install the update from:\n\n{file_path}")
                msg.exec()
                
        except Exception as e:
            QMessageBox.critical(self.parent, "Installation Error", f"Failed to install update:\n\n{str(e)}")
    
    def _install_from_zip(self, zip_path):
        """Install update from ZIP file"""
        try:
            # Extract to a temporary directory
            extract_dir = os.path.join(tempfile.gettempdir(), "pc-checker-update")
            if os.path.exists(extract_dir):
                shutil.rmtree(extract_dir)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            # Find the main executable or script
            main_file = None
            for root, dirs, files in os.walk(extract_dir):
                for file in files:
                    if file in ['script.py', 'main.py', 'pc-checker.exe', 'laptop-testing.exe']:
                        main_file = os.path.join(root, file)
                        break
                if main_file:
                    break
            
            if main_file:
                # Show installation instructions
                msg = QMessageBox(self.parent)
                msg.setWindowTitle("Update Extracted")
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setText(f"Update extracted to:\n{extract_dir}\n\nMain file: {os.path.basename(main_file)}\n\nWould you like to open the folder for manual installation?")
                msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                
                if msg.exec() == QMessageBox.StandardButton.Yes:
                    os.startfile(extract_dir)
            else:
                os.startfile(extract_dir)
                
        except Exception as e:
            QMessageBox.critical(self.parent, "Extraction Error", f"Failed to extract update:\n\n{str(e)}")
    
    def _set_update_reminder(self, update_info):
        """Set a reminder for the next startup"""
        try:
            reminder_file = os.path.join(os.path.dirname(__file__), "update_reminder.json")
            reminder_data = {
                'version': update_info['version'],
                'reminder_date': datetime.now().isoformat(),
                'update_info': update_info
            }
            
            with open(reminder_file, 'w') as f:
                json.dump(reminder_data, f, indent=2)
                
        except Exception as e:
            print(f"Failed to set update reminder: {e}")
    
    def check_update_reminder(self):
        """Check if there's a pending update reminder"""
        try:
            reminder_file = os.path.join(os.path.dirname(__file__), "update_reminder.json")
            if os.path.exists(reminder_file):
                with open(reminder_file, 'r') as f:
                    reminder_data = json.load(f)
                
                # Check if reminder is still relevant
                if pkg_version.parse(reminder_data['version']) > pkg_version.parse(self.current_version):
                    # Show reminder after a delay
                    QTimer.singleShot(3000, lambda: self._show_update_reminder(reminder_data['update_info']))
                else:
                    # Remove outdated reminder
                    os.remove(reminder_file)
                    
        except Exception as e:
            print(f"Failed to check update reminder: {e}")
    
    def _show_update_reminder(self, update_info):
        """Show the update reminder"""
        self._on_update_available(update_info)