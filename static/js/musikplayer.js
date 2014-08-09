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
  	$("#song-info-song").text(songs[current_index]['song-name']);
  	var song_id = songs[current_index]['id'];
  	$("#soundtrack-table > tbody > tr > td.song-id > div").each(function(index,value){
		if( song_id == $(value).attr("data-id")){
			$(value).parent().parent().css("background-color","#FFC970");
		}else{
			$(value).parent().parent().css("background-color","");
		}
	});
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

	wavesurfer.backend.on('audioprocess', function onFinish (time) {
        if (time >= ( wavesurfer.backend.getDuration() - 0.1)) {
           	console.log("finished");

			wavesurfer.un('audioprogress', onFinish);

			$("#next-button").trigger("click");
        }
    });

	//play();
	//wavesurfer.load(songs[current_index]['link']);
	load_and_play();
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

	$( "#prev-button" ).click(function() {
  		if( current_index == 0){
			current_index = songs.length -1;
		}else{
			current_index--;
		}
		load_and_play();
	});

	$( "#next-button" ).click(function() {
		if( current_index == (songs.length -1)){
			current_index = 0;
		}else{
			current_index++;
		}
		load_and_play();
	});

	$( ".soundtrack-play" ).click(function() {
		var song_id = $(this).attr("data-id");
		var i;
		for(i =0; i < songs.length; i++){
			if( songs[i]['id'] == song_id ){
				current_index = i;
				break;
			}
		}
		load_and_play();
	});
});


