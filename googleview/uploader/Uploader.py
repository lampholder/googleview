# This Python file uses the following encoding: utf-8
"""Utility class to handle uploading files to Google drive."""

from io import BytesIO

import unicodecsv

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.settings import LoadSettingsFile

class Uploader(object):
    """Handles upload of files to Google Drive. Other options were losing the file type on
    import and were uploading .csvs s Word documents :S."""

    def __init__(self, settings):
        gauth = GoogleAuth()
        gauth.settings = settings
        gauth.CommandLineAuth()
        self._drive = GoogleDrive(gauth)

    @classmethod
    def from_dict(cls, config_dict):
        """Instantiate the uploader with config supplied in a dict."""
        pass

    @classmethod
    def from_file(cls, config_filename):
        """Instantiate the uploader with config from a file."""
        settings = LoadSettingsFile(config_filename)
        return cls(settings)

    @staticmethod
    def __list_to_unicode_csv_string(data_list):
        """Convert a list of lists into a unicode CSV string"""
        #Holy guacamole this should *not* be so hard.
        encoding = 'utf-8'

        string_file = BytesIO()
        writer = unicodecsv.writer(string_file, encoding=encoding)

        for row in data_list:
            writer.writerow(row)

        return unicode(string_file.getvalue().decode(encoding))

    def upload_csv(self, parent_id, title, data):
        """Upload the contents to Google Drive"""

        unicode_data = self.__list_to_unicode_csv_string(data)

        # Check to see if the file already exists
        file_list = self._drive.ListFile({'q': '"%s" in parents and title="%s" and trashed=false'
                                               % (parent_id, title)}).GetList()

        # If file is found, update it, otherwise create new file
        if len(file_list) == 1:
            file_to_write_to = file_list[0]
        else:
            file_to_write_to = self._drive.CreateFile({"parents": [{"kind": "drive#fileLink",
                                                                    "id": parent_id}],
                                                       'mimeType':'text/csv'})

        file_to_write_to.SetContentString(unicode_data)
        file_to_write_to['title'] = title
        file_to_write_to.Upload({'convert': True})
