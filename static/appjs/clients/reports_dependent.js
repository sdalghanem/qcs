let report = document.getElementById("report")
// بدال البراند يصير البرانش يعني اذا اخترت الفرع تطلع لك التقارير حقته
branch.addEventListener('change', function() {
        report.style.display = 'inline'; // Show the city dropdown
        report.innerHTML = " ";
        report.innerHTML = "<option value='0'>اختر التقرير</option> ";
        //alert(brand.value)
///////////////////////////////////////////////////////////////
        $.ajax({
        type: 'post',
        url:'/clients/reports_list',
        async: true,
        data:{
        branch_id : branch.value,
        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
    } ,
    
        success:function(data){ 
         data.forEach((element) => {
            report.innerHTML += `
            <option value="${element.id}">( ${element.branch} ) ${element.date}</option>
            `;
         });
        },
        done:function(data){
            console.log('done ->>' + data)
        },
        error:function(data){
            console.log('error ->>' + data);

        }
});
    
});

// report.addEventListener('change', function() {
//     alert(report.value)
// });