from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string



def send_template_email(subject, to_email,template_name,context):
    """Send a message to a specific email address

    Args:
        subject (str): Email subject to send
        to_email (str): The email address to send to
        template_name (str): The template name to be used
        context (str): additional context data
    """

    html_content = render_to_string(template_name=f"email_templates/{template_name}.html",context=context)
    text_content = render_to_string(template_name=f"email_templates/{template_name}.txt",context=context)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email="Your Email@example.com",
        to=[to_email],
    )

    #attach email content
    email.attach_alternative(html_content, "text/html")

    email.send()





