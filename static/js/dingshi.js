function dingshi(){
    var maxTime = 180; // seconds
	var time = maxTime;
	$('body').on('keydown', function(e) {
			time = maxTime; // reset
	});
	var intervalId = setInterval(function() {
			time--;
			if (time <= 0) {
				ShowInvalidLoginMessage();
					clearInterval(intervalId);
				}
			}, 1000)
	function ShowInvalidLoginMessage() {
			$.ajax({
					type:"get",
					url:"/outsession",
					async:true,
					success:function(data){
					window.location.href="/";
					}
					});
			}
}