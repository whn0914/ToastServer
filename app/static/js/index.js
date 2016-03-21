$(document).ready(function() {
	$('input#insertInfo').click(function() {
		$('#qrcode').empty();
		var name = document.getElementById('name').value;
		var phone = document.getElementById('phone').value;
		if (name == undefined || phone == undefined || name.trim().length < 1 || phone.trim().length < 1) {
			alert("请输入姓名与电话");
			return false;
		}
		if (!(/^\d+$/.test(phone))) {
			alert("请输入正确的电话号码");
			return false;
		}

		$.ajax({
			url: '/scanner/insertInfo',
			type: 'get',
			dataType: 'json',
			data: $('form#info-form').serialize(),
			success: function(data) {
				var code = data.code;
				if (code != 1) {
					alert(data.msg);
				} else {
					// 生成二维码
					var info = data.data + '-' + phone;
					$('#qrcode').qrcode(info);
					alert("录入成功，请右键保存二维码");
				}
			}
		});
	});
})