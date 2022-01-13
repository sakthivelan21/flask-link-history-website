function playVideo(urlLink)
{
	var videoPlayer=document.getElementById('videoPlayer');
	if(videoPlayer.src==="")
	{
		videoPlayer.style['width']='0';
		videoPlayer.style['height']='0';
	}
	else
	{
		var link=urlLink.split('/');
        videoPlayer.src="https://www.youtube.com/embed/"+link[link.length-1];
        videoPlayer.style["width"]="80%";
        videoPlayer.style["height"]="400px";
	}	
}
