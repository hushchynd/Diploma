import {upload} from "./upload_html.js";
upload('.file-html',{
    multiple: false,
    accept: ['.html']
})
$('.form__elem_radio').each(function () {
    if ($(this).attr('checked')){
        $(this).parent().parent().css({
        background:'#00B894'
        })
    }
})
$('.form__elem_radio').on('mousedown','div',function (event) {

    $(this).find('input').click();

    $(this).parent().children().css({
        background:'#6C5CE7'
    })
    $(this).css({
        background:'#00B894'
    })
})
$('#selected_clients').on('change',function () {
    if ($(this).attr('checked',true)){
        $('.card__btn').css({
            display: 'block'
        })
    }

})
$('#all_clients').on('change',function () {
    if ($(this).attr('checked',true)){
        $('.card__btn').css({
            display: 'none'
        })
    }

})
$('.file-html').attr('required',false)
$("input[name='template']").on('change',function () {
    if ($(this).attr('id')==='new_template'){
        $('.card__file').css({
            display: 'flex'
        })
        $('.card__list').css({
            display: 'none'
        })
    }else{
        $('.card__file').css({
            display: 'none'
        })
        $('.card__list').css({
            display: 'flex'
        })
    }

})