var wavesurfer = Object.create(WaveSurfer);
var songs;
var current_index = 0;

function loadSongs(json){
	songs = json;
}

function play(){
	wavesurfer.on('ready', function () {
	$("#loading").css("opacity","0");
    	$("#wave").css("opacity","1");
    	wavesurfer.play();
	});
}

function load_and_play(){
	$("#loading").css("opacity","1");
    $("#wave").css("opacity","0");
	wavesurfer.load(songs[current_index]['link']);
  	play();

}

$(function() {
	wavesurfer.init({
		container: document.querySelector('#wave'),
		waveColor: '#FFC970',
		progressColor: '#FF9F00',
		cursorColor:'grey',
		markerWidth: 2,
		dragSelection : false,
		loopSelection : false,
	});

	$( "#play-button" ).click(function() {
		$("#play-button").css("display","none");
		$("#pause-button").css("display","block");
		wavesurfer.play();
	});

	$( "#pause-button" ).click(function() {
		$("#play-button").css("display","block");
		$("#pause-button").css("display","none");
		wavesurfer.pause();
	});

});


