from captcha.fields import CaptchaTextInput


class BootstrapCaptchaTextInput(CaptchaTextInput):
    template_name = 'core/bootstrap_captcha_text_field.html'
