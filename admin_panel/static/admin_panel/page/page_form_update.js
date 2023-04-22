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

$('.on_off').parent().hide()
if($('.on_off').is(':checked')){
    $('input[role=\'switch\']').attr('checked',true)
}

$('input[role=\'switch\']').on('click',function () {
    if ($(this).is(':checked')){
        $('.on_off').attr('checked',true)

    }else{
        $('.on_off').attr('checked',false)


    }

})