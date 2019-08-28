from datetime import time
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from complaints.models import Complaint

# , UnblockRequest


class TestComplaint(TestCase):
    def setUp(self):
        User = get_user_model()
        u1 = User(username="tester", email="tester@tester.dev")
        u1.set_password("tester")
        u1.save()
        Complaint.objects.create(
            user=u1,
            category=Complaint.CATEGORY_1,
            status=Complaint.REGISTERED,
            uploaded_at=timezone.now(),
            remark="Bla Bla Wifi Problem",
            contact_no="9756345621",
            room_no="R045",
            avail_start_time=time(hour=12, minute=35, second=0),
            avail_end_time=time(hour=15, minute=35, second=0),
        )

    def test_complaint_str(self):
        comp = Complaint.objects.get(pk=1)
        self.assertEqual(str(comp), f"{comp.user} - {comp.category} - {comp.id}")

    def test_complaint_save_correct(self):
        user = get_user_model().objects.get(username="tester")
        Complaint.objects.create(
            user=user,
            category=Complaint.CATEGORY_2,
            status=Complaint.REGISTERED,
            uploaded_at=timezone.now(),
            remark="Bla Bla Wifi Problem",
            contact_no="97556345621",
            room_no="B069",
            avail_start_time=time(hour=2, minute=31, second=0),
            avail_end_time=time(hour=5, minute=35, second=0),
        )
        comp = Complaint.objects.get(category=Complaint.CATEGORY_2)
        self.assertEqual(comp.pk, 2)
        self.assertEqual(comp.user, user)

    def test_complaint_save_urgent(self):
        user = get_user_model().objects.get(username="tester")
        Complaint.objects.create(
            user=user,
            category=Complaint.CATEGORY_3,
            status=Complaint.REGISTERED,
            uploaded_at=timezone.now(),
            remark="Bla Bla Wifi Problem",
            contact_no="97556345621",
            room_no="B069",
            urgency=True,
            urgency_reason="It's me!",
            avail_start_time=time(hour=2, minute=31, second=0),
            avail_end_time=time(hour=5, minute=35, second=0),
        )
        comp = Complaint.objects.get(category=Complaint.CATEGORY_3)
        self.assertEqual(comp.pk, 2)
        self.assertEqual(comp.user, user)

    def test_avail_time_at_least_one_hour(self):
        user = get_user_model().objects.get(username="tester")
        with self.assertRaisesMessage(
            ValidationError, "Available time is less than one hour."
        ):
            Complaint.objects.create(
                user=user,
                category=Complaint.CATEGORY_2,
                status=Complaint.REGISTERED,
                uploaded_at=timezone.now(),
                remark="Bla Bla Wifi Problem",
                contact_no="97556345621",
                room_no="B069",
                avail_start_time=time(hour=2, minute=31, second=0),
                avail_end_time=time(hour=2, minute=35, second=0),
            )

    def test_urgency_reason_present_if_urgent(self):
        user = get_user_model().objects.get(username="tester")
        with self.assertRaisesMessage(
            ValidationError, "No urgency reason given for urgent complaint."
        ):
            Complaint.objects.create(
                user=user,
                category=Complaint.CATEGORY_1,
                status=Complaint.REGISTERED,
                uploaded_at=timezone.now(),
                remark="Bla Bla Wifi Problem",
                urgency=True,
                contact_no="97556355621",
                room_no="VK092",
                avail_start_time=time(hour=5, minute=31, second=0),
                avail_end_time=time(hour=7, minute=35, second=0),
            )
        with self.assertRaisesMessage(
            ValidationError, "No urgency reason given for urgent complaint."
        ):
            Complaint.objects.create(
                user=user,
                category=Complaint.CATEGORY_1,
                status=Complaint.REGISTERED,
                uploaded_at=timezone.now(),
                remark="Bla Bla Wifi Problem",
                urgency=True,
                urgency_reason="",
                contact_no="97556355621",
                room_no="VK092",
                avail_start_time=time(hour=5, minute=31, second=0),
                avail_end_time=time(hour=7, minute=35, second=0),
            )

    # TODO: Write
    def test_user_can_only_cancel_complaint(self):
        user = get_user_model().objects.get(username="tester")
        comp = Complaint.objects.get(pk=1)

