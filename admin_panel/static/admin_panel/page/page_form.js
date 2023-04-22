import {upload} from "../../js/upload.js";

upload('.form__horizontal-img',{
    multiple: false,
    accept: ['.png','.jpg','.jpeg','.svg']
})
upload('.form__horizontal-img_2',{
    multiple: false,
    accept: ['.png','.jpg','.jpeg','.svg']
})
upload('.form__horizontal-img_3',{
    multiple: false,
    accept: ['.png','.jpg','.jpeg','.svg']
})
upload('.form__horizontal-img_4',{
    multiple: false,
    accept: ['.png','.jpg','.jpeg','.svg']
})
upload('.form__input-file-multi',{
    multiple: true,
    accept: ['.png','.jpg','.jpeg','.svg']
})
$('.on_off').parent().hide()

$('input[role=\'switch\']').on('click',function () {
    if ($(this).is(':checked')){
        $('.on_off').attr('checked',true)

    }else{
        $('.on_off').attr('checked',false)


    }

})