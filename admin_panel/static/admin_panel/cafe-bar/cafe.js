let cafeTotalForms = $('#id_form-TOTAL_FORMS')

$('.btn-add').on('click',function (event) {
    let newRow = $(`
       <tr>
           <td><input type="text" name="form-${cafeTotalForms.val()}-name" maxlength="150" id="id_form-${cafeTotalForms.val()}-name"></td>
           <td><input type="number" name="form-${cafeTotalForms.val()}-weight" min="0" id="id_form-${cafeTotalForms.val()}-weight"></td>
           <td><input type="number" name="form-${cafeTotalForms.val()}-price" min="0" id="id_form-${cafeTotalForms.val()}-price"></td>                        
           <input type="hidden" name="form-${cafeTotalForms.val()}-id" id="id_form-${cafeTotalForms.val()}-id">
           <td>
               <input type="checkbox" name="form-${cafeTotalForms.val()}-DELETE" id="id_form-${cafeTotalForms.val()}-DELETE" hidden>
               <img class="table__icon btn-remove" src="/static/admin_panel/imgs/delete.png" alt="">
           </td>
       </tr>
    `)

    cafeTotalForms.val(Number(cafeTotalForms.val())+1)
    $('.table').append(newRow)
})

$("[name$='DELETE'], [for$='DELETE']").hide()
$('.table').on('click','.btn-remove',function (event) {
    alert('hello')
    $(this).siblings('[name$=\'DELETE\']').attr('checked','checked')
    $(this).parents("tr:first").fadeOut("slow", function() {
    // Animation complete.
  })

})