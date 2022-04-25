import json
import os

from django import forms
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from oppia.test import OppiaTestCase


class MediaAPIResourceTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_av_uploadedmedia.json',
                'tests/test_course_permissions.json']

    def setUp(self):
        super(MediaAPIResourceTest, self).setUp()
        self.url = '/api/media/'
        self.get_valid_digest = '/api/media/3f2d7d54e969e303901ba5a177bd2334'
        self.get_invalid_digest = '/api/media/123456789'
        self.course_file_path = os.path.join(settings.TEST_RESOURCES, 'ncd1_test_course.zip')
        self.video_file_path = os.path.join(settings.TEST_RESOURCES, 'sample_video.m4v')

    # test only POST is available
    def test_no_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    # test all params have been sent
    def test_required_params(self):

        # no username
        with open(self.video_file_path, 'rb') as video_file:
            response = self.client.post(self.url,
                                        {'password': 'secret',
                                         'media_file': video_file})
        self.assertRaises(forms.ValidationError)
        self.assertEqual(response.status_code, 400)

        # no password
        with open(self.video_file_path, 'rb') as video_file:
            response = self.client.post(self.url,
                                        {'username': 'demo',
                                         'media_file': video_file})
        self.assertEqual(response.status_code, 400)

    # check authentication check working correctly
    def test_authentication(self):

        # incorrect username
        with open(self.video_file_path, 'rb') as video_file:
            response = self.client.post(self.url,
                                        {'username': 'demouser',
                                         'password': 'password',
                                         'media_file': video_file})
        self.assertEqual(response.status_code, 401)

        # incorrect password
        with open(self.video_file_path, 'rb') as video_file:
            response = self.client.post(self.url,
                                        {'username': 'demo',
                                         'password': 'wrong_password',
                                         'media_file': video_file})
        self.assertEqual(response.status_code, 401)

    # test is user has correct permissions or not to upload
    def test_permissions(self):
        # set to inactive user
        user = self.normal_user
        user.is_active = False
        user.save()

        with open(self.video_file_path, 'rb') as video_file:
            response = self.client.post(self.url,
                                        {'username': 'demo',
                                         'password': 'password',
                                         'media_file': video_file})

        self.assertEqual(response.status_code, 401)

        # set back to active user
        user.is_active = True
        user.save()

    # check upload works for all users
    def test_upload_user(self):

        # normal user
        with open(self.video_file_path, 'rb') as video_file:
            upload_file = SimpleUploadedFile(video_file.name,
                                             video_file.read(),
                                             content_type='video/mp4')
            response = self.client.post(self.url, {'username': 'demo',
                                                   'password': 'password',
                                                   'media_file': upload_file})
        self.assertEqual(response.status_code, 201)

    def test_upload_teacher(self):
        # teacher
        with open(self.video_file_path, 'rb') as video_file:
            upload_file = SimpleUploadedFile(video_file.name,
                                             video_file.read(),
                                             content_type='video/mp4')
            response = self.client.post(self.url, {'username': 'teacher',
                                                   'password': 'password',
                                                   'media_file': upload_file})
        self.assertEqual(response.status_code, 201)

    def test_upload_staff(self):
        # staff
        with open(self.video_file_path, 'rb') as video_file:
            upload_file = SimpleUploadedFile(video_file.name,
                                             video_file.read(),
                                             content_type='video/mp4')
            response = self.client.post(self.url, {'username': 'staff',
                                                   'password': 'password',
                                                   'media_file': upload_file})
        self.assertEqual(response.status_code, 201)

    def test_upload_admin(self):
        # admin
        with open(self.video_file_path, 'rb') as video_file:
            upload_file = SimpleUploadedFile(video_file.name,
                                             video_file.read(),
                                             content_type='video/mp4')
            response = self.client.post(self.url, {'username': 'admin',
                                                   'password': 'password',
                                                   'media_file': upload_file})
        self.assertEqual(response.status_code, 201)

    # test file type
    def test_filetype(self):

        with open(self.course_file_path, 'rb') as course_file:
            # send zip file
            response = self.client.post(self.url,
                                        {'username': 'demo',
                                         'password': 'password',
                                         'media_file': course_file})
        self.assertEqual(response.status_code, 400)

    def test_digest_valid(self):
        response = self.client.get(self.get_valid_digest)
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content)

        self.assertEqual(json_data['digest'],
                         "3f2d7d54e969e303901ba5a177bd2334")
        self.assertEqual(json_data['filesize'], 0)
        url = "http://testserver/media/uploaded/2018/02/MH1_Keyboard_480p.mp4"
        self.assertEqual(json_data['download_url'], url)
        self.assertEqual(json_data['length'], 170)

    def test_digest_invalid(self):
        response = self.client.get(self.get_invalid_digest)
        self.assertEqual(response.status_code, 404)
