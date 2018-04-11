import click
import delegator

@click.command()
@click.option('--source')
@click.option('--output')
def dashify(source, output):
	x264_template = 'x264 --output tmp_{bitrate}.264 --fps 24 --preset slow --bitrate {bitrate} --vbv-maxrate {bitrate2} \
	--vbv-bufsize {bitrate4} --min-keyint 96 --keyint 96 --scenecut 0 --no-scenecut --pass 1 --video-filter \
	"resize:width={width},height={height}" "{source}"'
	mp4_template = 'MP4Box -add tmp_{bitrate}.264 -fps 24 {output}_{bitrate}.mp4'
	dash_template = 'MP4Box -dash 4000 -frag 4000 -rap -segment-name segment{bitrate}_ {output}_{bitrate}.mp4'
	audio_template = 'ffmpeg -i "{source}" -vn -acodec libvorbis -ab 320k -dash 1 {output}_audio.webm'
	audio_manifest = 'ffmpeg \
	-f webm_dash_manifest -i {output}_audio.webm -c copy -map 0 \
	-f webm_dash_manifest -adaptation_sets "id=0,streams=0" {output}_audio_manifest.mpd'
	
	parameters = [(640, 360, 350), (854, 480, 750), (1280, 720, 2400), (1920, 1080, 5000)]
	
	print 'Starting audio processing'
	audio = audio_template.format(source=source, output=output)
	a_manifest = audio_manifest.format(source=source, output=output)
	delegator.run(audio)
	delegator.run(a_manifest)
	
	print 'Starting video processing'
	for width, height, bitrate in parameters:
		print 'Processing {}/{}-{}'.format(width, height, bitrate)
		arg_dict = {
			'source': source,
			'output': output,
			'bitrate': bitrate,
			'bitrate2': bitrate * 2,
			'bitrate4': bitrate * 4,
			'width': width,
			'height': height,
		}
		x264 = x264_template.format(**arg_dict)
		mp4 = mp4_template.format(**arg_dict)
		dash = dash_template.format(**arg_dict)
		delegator.run(x264)
		delegator.run(mp4)
		delegator.run(dash)
		delegator.run('rm -rf tmp_{bitrate}.264 {output}_{bitrate}.mp4'.format(**arg_dict))
		
dashify()
	

