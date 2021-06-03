from captcha.fields import CaptchaTextInput


class BootstrapCaptchaTextInput(CaptchaTextInput):
    def __init__(self):
        super().__init__(attrs={'class':'textinput textInput form-control'})
