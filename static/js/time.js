function gettime(){
    var date = new Date();
    var year = date.getFullYear();
    var month = date.getMonth() + 1;
    var day = date.getDate();
    var hours=date.getHours();
    var Minutes=date.getMinutes();
    var Seconds=date.getSeconds();
    if (month < 10) {
        month = "0" + month;
    }
    if (day < 10) {
        day = "0" + day;
    }
    if (hours < 10) {
        hours = "0" + hours;
    }
    if (Minutes < 10) {
       Minutes = "0" + Minutes;
    }
    if (Seconds < 10) {
        Seconds = "0" +Seconds;
    }
    times = year + "-" + month + "-" + day+" "+hours+":"+Minutes+":"+Seconds;
}