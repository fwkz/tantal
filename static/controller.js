$(document).ready(function(){
    var sock = null;
    var wsuri = "ws://192.168.1.1:8080/ws";

    sock = new WebSocket(wsuri);

    sock.onopen = function() {
        console.log("connected to " + wsuri);
    };

    sock.onclose = function(evt) {
        console.log("connection closed (" + evt.code + ")");
    };

    sock.onmessage = function(evt) {
        $("#box").text(evt.data);
        console.log("message received: " + evt.data);
    };


    function press(keyID){
        sock.send(keyID)
    };

    function release(){
        sock.send("0")
    };

    var pressed = false;

    $(document).keydown(function(evt){
        if (pressed == false) {
            var keyID =  evt.which || evt.key || evt.which;
            press(keyID);
        }
        pressed = true;
    });

    $(document).keyup(function(){
        pressed = false;
        release();
    });

    $(".button").on("vmousedown", function(evt){
//        alert("pressed")
        press(evt.target.id);
    }).on("vmouseup", function(){
//          alert("relese");
        release();
    });
});