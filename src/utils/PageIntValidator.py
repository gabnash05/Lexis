from PyQt6.QtGui import QIntValidator

class PageIntValidator(QIntValidator):
  def fixup(self, input_str: str) -> str:
    if not input_str.isdigit():
      return str(self.bottom())
    num = int(input_str)
    if num < self.bottom():
      return str(self.bottom())
    if num > self.top():
      return str(self.top())
    return input_str