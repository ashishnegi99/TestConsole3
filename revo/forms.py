from django import forms
from django.forms import ModelForm
from revo.models import device

class DeviceForm(forms.Form):
	device_name = forms.CharField(label="device name", max_length=200, widget=forms.TextInput(attrs={'class': "form-control input-sm"}))
	subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': "form-control input-sm"}))
	message = forms.CharField(widget=forms.Textarea)
	sender = forms.EmailField()
	cc_myself = forms.BooleanField(required=True)

class DeviceMForm(ModelForm):
 	class Meta:
 		model = device
 		#fields = ['name', 'mac_id', 'serial_id', 'device_type', 'router', 'host']
 		exclude = []

	def __init__(self, *args, **kwargs):
		super(DeviceMForm, self).__init__(*args, **kwargs)
		for k in self.fields:
			self.fields[k].widget.attrs.update({
					'class': 'form-control input-sm'
				})