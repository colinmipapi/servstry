function getExif(newimg, id, file) {
    EXIF.getData(file, function() {
            var orientation = EXIF.getTag(this, "Orientation");
            if(orientation == 6) {
                newimg.className = "camview rotate90";
                if (id==='coverSampleImg'){
                    $(newimg).attr('height', '')
                }
            } else if(orientation == 8) {
                newimg.className = "camview rotate270";
                if (id==='coverSampleImg'){
                    $(newimg).attr('height', '100%')
                }
            } else if(orientation == 3) {
                newimg.className = "camview rotate180";
                if (id==='coverSampleImg'){
                    $(newimg).attr('height', '')
                }
            }
    });
};