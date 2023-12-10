"""Module for app logic."""
from django.core.mail import send_mail

def mail(lab, email, passed):
    """
        send notification to student when report is graded
    """
    if passed:
        subject = 'Raporttisi on arvioitu'
        message = (
            f'Raporttisi työhön {lab} on arvioitu.\n'
            f'Arviointia pääsee tarkastelemaan palautussovelluksesta.'
        )
        send_mail(
            subject,
            message,
            'grp-fyskem-labra-ilmo@helsinki.fi',
            [email],
            fail_silently=False
        )
    else:
        subject = 'Raporttisi vaatii korjausta'
        message = (
            f'Raporttisi työhön {lab} on arvioitu ja se vaatii korjausta.\n'
            f'Kommentit ja korjausehdotukset löytyvät palautussovelluksesta.'
        )
        send_mail(
            subject,
            message,
            'grp-fyskem-labra-ilmo@helsinki.fi',
            [email],
            fail_silently=False
        )
