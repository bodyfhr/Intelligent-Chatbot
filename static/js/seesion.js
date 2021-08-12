function getsession(){
    see=Math.ceil(1000000000*Math.random());
        $.ajax({
                type:"get",
                url:"/yonghu",
                async:true,
                data:{'user':see},
                success:function(){
                window.location.href="/";
                }
                });
}