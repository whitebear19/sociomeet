jQuery(function ($) {

    'use strict';
    var user_name = '';
    var invite_user_array = [];
   
// ----------------------------------------------------------------
   


    (function() {
        function slider_reset()
        {     
            $('.regular').slick('unslick');
            $(".regular").slick({
                dots: true,
                infinite: true,
                slidesToShow: 2,
                slidesToScroll: 2,                     
                responsive: [                            
                    {
                    breakpoint: 600,
                    settings: {
                        slidesToShow: 1,
                        slidesToScroll: 1
                    }
                    }
                    
                ]
            });   
        }

        function img_slider()
        {        
            slideLeft = 0 - curSlidePos*item_width;
            $('.uploaded_files').css('left',slideLeft);
        }

        $(document).on('click','.btn_user_nav',function(){
            
            var item = $(this).data('item');
            $('.btn_user_nav').removeClass('selecte_nav');           
            $(this).addClass('selecte_nav');    
            $(".content_user_nav").addClass('display_none');
            $("#user_"+item).removeClass('display_none');
            $.cookie('nav', item);
            slider_reset();
        });

        $(document).on('click','.btn_add_benefit',function(){
            
            var value = $(".input_add_benefit").val();
            if(value == "")
            {
                return false;
            }
            var html=`
                <li>
                    <div>
                        <input type="checkbox"  class="input_benefit" name="benefit_item[]" value="${value}">
                        <span for="">${value}</span>
                    </div>
                </li>
            `;
            $(".added_benefit").append(html);
            $(".input_add_benefit").val("");
        });

        $(document).on('click','.btn_job_step',function(){
            var chk_result = true;
            var cur = $(this).data('cur');
            $(".job_content_"+cur+" .required_field").each(function(){
                if($(this).val() == "")
                {
                    $(this).addClass("alert-border");
                    chk_result = false;
                }
            });
            var value = $(this).data('nav');
            if(chk_result)
            {
                $(".job_input_step_nav").removeClass("selected_nav");
                $(".job_content_item").removeClass("selected_nav_content");
                
                $(".job_"+value).addClass("selected_nav");
                $(".job_content_"+value).addClass("selected_nav_content");
                var benefits = '';
                var work_auth = '';
                if(value == "preview")
                {
                    $("#job_title_publish").html($(".input_job_title").val());
                    $("#job_description_publish").html($(".input_job_description").val());
                    $(".input_benefit").each(function(){
                        if(this.checked) {
                           if(benefits == "")
                           {
                               benefits+=$(this).val();
                           }
                           else
                           {
                                benefits+=", "+$(this).val();
                           }
                        }
                    });

                    $(".input_work_auth").each(function(){
                        if(this.checked) {
                           if(work_auth == "")
                           {
                                work_auth+=$(this).val();
                           }
                           else
                           {
                                work_auth+=", "+$(this).val();
                           }
                        }
                    });
                    
                    $(".job_info_benefits_publish").html(benefits);
                    $(".job_info_benefits_publish_input").val(benefits);
                    if(benefits == "")
                    {
                        $(".part_benefits").css("display","none");
                    }
                    else
                    {
                        $(".part_benefits").css("display","block");
                    }
                    if(work_auth == "")
                    {
                        $(".part_workauth").css("display","none");
                    }
                    else
                    {
                        $(".part_workauth").css("display","block");
                    }
                    if(benefits=="" && work_auth =="")
                    {
                        $(".part_benefits_workauth").css("display","none");
                    }
                    else
                    {
                        $(".part_benefits_workauth").css("display","block");
                    }
                    $(".job_info_workauth_publish").html(work_auth);
                    $(".job_info_workauth_publish_input").val(work_auth);
                    $(".job_info_postedby_publish").html(user_name);  
                    var currentdate = new Date();                   
                    $(".job_info_postedon_publish").html(currentdate.getDate() + "/" + (currentdate.getMonth()+1)  + "/" + currentdate.getFullYear());                    
                    
                    autosize(document.getElementById("job_description_publish"));
                    $(".job_info_client_publish").html($(".input_client").val());                      
                    $(".job_info_travel_publish").html($(".input_travel").val());   
                    $(".job_info_salary_publish").html($(".salary_price").val()+"/"+$(".salary_period").val());   
                    $(".job_info_remote_publish").html($(".input_remote").val());   
                    $(".job_info_type_publish").html($(".input_type").val());   
                    
                    if($(".input_client").val()=="")
                    {
                        $(".part_client").css("display",'none');
                    }
                    else
                    {
                        $(".part_client").css("display",'block');
                    }
                    if($(".input_travel").val()=="")
                    {
                        $(".part_travel").css("display",'none');
                    }
                    else
                    {
                        $(".part_travel").css("display",'block');
                    }
                    if($(".salary_price").val()=="")
                    {
                        $(".part_salary").css("display",'none');
                    }
                    else
                    {
                        $(".part_salary").css("display",'block');
                    }
                    if($(".input_remote").val()=="")
                    {
                        $(".part_remote").css("display",'none');
                    }
                    else
                    {
                        $(".part_remote").css("display",'block');
                    }
                    if($(".input_type").val()=="")
                    {
                        $(".part_type").css("display",'none');
                    }
                    else
                    {
                        $(".part_type").css("display",'block');
                    }

                }
            }
            else
            {
                return false;
            }
        });
        
        $(document).on('click','.btn_select_job_view',function(){            
            var which = $(this).data('value');
            $(".btn_select_job_view").removeClass("btn_selected_job_view");
            $(".job_list_view").removeClass("job_list_view_selected");
            $(".btn_select_job_view_"+which).addClass("btn_selected_job_view");
            $(".job_list_"+which).addClass("job_list_view_selected");
        });
        
        
        $('.chk_reply_item').change(function() {
            var value = $(this).data('value');
            
            if(this.checked) {
                $(".input_reply_item_"+value).attr("disabled",false);
                $(".input_reply_item_"+value).addClass("required_field");
                $('#reply_not').prop('checked', false);
            }
            else
            {
                $(".input_reply_item_"+value).val('');
                $(".input_reply_item_"+value).attr("disabled",true);
                $(".input_reply_item_"+value).removeClass("required_field");
            }       
        });
        
        $('#reply_not').change(function() {
            
            if(this.checked) {
                $('.chk_reply_item').prop('checked', false);
                $(".input_reply_item").attr("disabled",true);                
                $(".input_reply_item").val('');
                $(".input_reply_item").removeClass("required_field");
                $(".input_reply_item").removeClass("alert-border");
            }               
        });
        



        function emojiPickerInit()
        {
            $('#post_content').emojiPicker({
                width: '300px',
                height: '200px',
                button: false
            });
            $('#post_content').emojiPicker('toggle');
            $('#post_content').emojiPicker('toggle');
        }


        $(document).ready(function(){
            emojiPickerInit();
            user_name = $(".user_full_name").html();
            if($.cookie('nav') !="")
            {
                var item = $.cookie('nav');  
                $('.btn_user_nav').removeClass('selecte_nav');
                $("button[data-item='" + item +"']").addClass('selecte_nav');   
                $(".content_user_nav").addClass('display_none');
                $("#user_"+item).removeClass('display_none');                
                slider_reset();
            }
            $('#btn_emojis').click(function(e) {
                e.preventDefault();
                
                $('#post_content').emojiPicker('toggle');
            });
            var cur_url = window.location.href;            
            if (cur_url.indexOf("group") >= 0)
            {                
                $(".sub_menu_item").removeClass("selected_sub_menu");
                $(".sub_menu_item_group").addClass("selected_sub_menu");
            }
            else if(cur_url.indexOf("page") >= 0)
            {
                $(".sub_menu_item").removeClass("selected_sub_menu");
                $(".sub_menu_item_page").addClass("selected_sub_menu");
            }
            else if(cur_url.indexOf("job") >= 0)
            {
                $(".sub_menu_item").removeClass("selected_sub_menu");
                $(".sub_menu_item_job").addClass("selected_sub_menu");
            }
            else if(cur_url.indexOf("trending") >= 0)
            {
                $(".sub_menu_item").removeClass("selected_sub_menu");
                $(".sub_menu_item_trending").addClass("selected_sub_menu");
            }
            else
            {
                $(".sub_menu_item").removeClass("selected_sub_menu");
            }
        });
        
    }());

 

    (function () {
        function readURL(input) {
            if (input.files && input.files[0]) {
              var reader = new FileReader();
              
              reader.onload = function(e) {
                $('.preview_image').attr('src', e.target.result);
              }
              
              reader.readAsDataURL(input.files[0]); // convert to base64 string
            }
          }
          
          $(".select_img_preview").change(function() {
            readURL(this);
          });
          $(document).on('click','.alert-border',function() {
            $(this).removeClass("alert-border");
          });
          
    }());

    (function () {
        $(document).on('click','.post_item_view',function(){
            var pid = $(this).data('pid');
            $.ajax({                
                url:"/set_view",
                type: 'get',
                dataType: 'json',
                data: {pid:pid},

                success: function(response){
                    
                }
            });
        });
    }());   
    
    (function () {
       
        $(document).on('click','.btn_clear_preview',function(){
            $(".preview_image").attr("src","/static/img/camera.png");
            $("#group_img").val("");
        }); 

        $(document).on('click','.btn_group_like',function(){
            var likes = parseInt($(this).find("span.likes").html());
            if($(this).find('i.fa-heart').hasClass('far'))
            {
                $(this).find("span.likes").html(likes+1);
                $(this).find('i.fa-heart').removeClass('far');
                $(this).find('i.fa-heart').addClass('fas');
            }
            else
            {
                if(likes>0)
                {
                    $(this).find("span.likes").html(likes-1);
                }
                $(this).find('i.fa-heart').removeClass('fas');
                $(this).find('i.fa-heart').addClass('far');
            }
            var id = $(this).data('id');
            $.ajax({
                url: "/group/set_group_like",
                method: 'GET', 
                type: 'json',
                data: {id:id},     
                success: function(response){    
                           
                    if(!response.results)
                    {
                        swal({
                            title: "Something wrong!",  
                            text: "Please try again.",                          
                            type: "error"
                        }).then(function() {
                            location.reload();
                        });
                    }
                }
            })
        });

        $(document).on('click','.btn_page_like',function(){
            var likes = parseInt($(this).find("span.likes").html());
            if($(this).find('i.fa-heart').hasClass('far'))
            {
                $(this).find("span.likes").html(likes+1);
                $(this).find('i.fa-heart').removeClass('far');
                $(this).find('i.fa-heart').addClass('fas');
            }
            else
            {
                if(likes>0)
                {
                    $(this).find("span.likes").html(likes-1);
                }
                $(this).find('i.fa-heart').removeClass('fas');
                $(this).find('i.fa-heart').addClass('far');
            }
            var id = $(this).data('id');
            $.ajax({
                url: "/page/set_page_like",
                method: 'GET', 
                type: 'json',
                data: {id:id},     
                success: function(response){    
                           
                    if(!response.results)
                    {
                        swal({
                            title: "Something wrong!",  
                            text: "Please try again.",                          
                            type: "error"
                        }).then(function() {
                            location.reload();
                        });
                    }
                }
            })
        });


        // invite_modal_part
        $(document).on('click','.btn_modal_invite',function(){
            $("#inviteUser").modal('hide');
        });
        $(document).on('click','.btn_cancel_invite',function(){
            $('input[type=checkbox]:checked').each(function() {
                $(this).prop('checked',false);                             
            });    
        });
        function get_UserForInvite()
        {
            var search_word = $(".search_word_for_invite").val();
            
            $.ajax({
               url: "/get_UserForInvite",
               method: 'GET',
               type: 'json',
               data: {search_word:search_word},
               success: function(response) 
               {
                  var html = '';   
                  console.log(response);
                  var data = response.results;
                  $(".invite_user_area_modal").html("");
                  if(data.length>0)
                  {
                     for(var i=0;i<data.length;i++)
                     {
                        html+=` 
                           <div class="custom-control custom-checkbox mb-2">
                                <input type="checkbox" class="custom-control-input list_user_id" name="user_id" id="user_id_${data[i].id}" value="${data[i].id}">
                                <label class="custom-control-label invite_userlist" for="user_id_${data[i].id}">
                                    <div class="d-flex align-items-center osahan-post-header people-list">
                                        <div class="dropdown-list-image mr-3">                                            
                                            <img class="rounded-circle" src="${data[i].avatar}">                                              
                                        </div>
                                        <div class="font-weight-bold mr-2">
                                            <div class="text-truncate"><span class="text-blue">${data[i].firstname}&nbsp;${data[i].lastname}</span></div>
                                            <div class="small text-gray-500">
                                            </div>
                                        </div>                                                        
                                    </div>
                                </label>
                            </div>
                        `;
                     }
                  }
                  else
                  {
                     html+=`
                        <p>
                           There is no data to match.
                        </p>
                     `;
                  }
                  $(".invite_user_area_modal").append(html);
                  
               }
            });           
        }
        // invite_modal_part >>>> search user
        $('.search_word_for_invite').keypress(function(event){
            var keycode = (event.keyCode ? event.keyCode : event.which);
            if(keycode == '13'){
              get_UserForInvite();
            }                
        });
        $(document).on('click','.btn_search_user_for_invite',function(){   
            get_UserForInvite();
        });
        
        $(document).on('click','.btn_delete_noti',function(){   
            var id = $(this).data('id');
            if(id != "")
            {
                $(".notification_"+id).remove();
                var cnt_notification = parseInt($('.cnt_notification').html());
                if(cnt_notification > 0)
                {
                    $('.cnt_notification').html(cnt_notification-1);
                }
                
                $.ajax({
                    url: "/delete_notification",
                    method: 'GET',
                    type: 'json',
                    data: {id:id},
                    success: function(response) 
                    {

                    }
                });
            }            

        });

        $(document).on('click','.notification_unread .notification_set_read',function(){   
            var id = $(this).data('id');
            
            if(id != "")
            {                
                $.ajax({
                    url: "/notification_set_read",
                    method: 'GET',
                    type: 'json',
                    data: {id:id},
                    success: function(response) 
                    {
                        if(response.results)
                        {                            
                            var temp = $(".notification_"+id).html();
                            var html = '<div class="pos_rel notification_set_read notification_unread_item notification_'+id+'" data-id="'+id+'">';
                            html += temp;
                            html += '</div>';
                            $(".notification_read").prepend(html);
                            $(".notification_"+id).remove();
                            var cnt_notification = parseInt($(".cnt_notification").html());
                            if(cnt_notification>0)
                            {
                                $(".cnt_notification").html(cnt_notification-1);
                            }
                        }
                    }
                });
            }            

        });
        
        
    }());  
   
    // ------------------------Gif Input part------------------------

    (function () {        
        $(document).on('click','.btn_gif_input',function(){
            $("#gifInput").modal('toggle');
        });

        $(document).on('click','.gif_item_img',function(){
            var name = $(this).data('name');
            $.ajax({
                url: "/store_gif",
                method: 'GET',
                type: 'json',
                data: {name:name},
                success: function(response) 
                {
                    
                    var data = response.attachname;
                    console.log(data);  
                    var fileExt = data.split(".")[1];
                    let html = '<div class="uploaded_files_item">';                    
                    html += '<img src="/media/'+data+'" alt="">';                    
                    html += '<button class="btn_transparent btn_delete_uploadedFile"><svg style="width:15px;height:15px;" aria-hidden="true" focusable="false" data-prefix="fas" data-icon="times" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 352 512" class="svg-inline--fa fa-times fa-w-11 fa-3x"><path fill="currentColor" d="M242.72 256l100.07-100.07c12.28-12.28 12.28-32.19 0-44.48l-22.24-22.24c-12.28-12.28-32.19-12.28-44.48 0L176 189.28 75.93 89.21c-12.28-12.28-32.19-12.28-44.48 0L9.21 111.45c-12.28 12.28-12.28 32.19 0 44.48L109.28 256 9.21 356.07c-12.28 12.28-12.28 32.19 0 44.48l22.24 22.24c12.28 12.28 32.2 12.28 44.48 0L176 322.72l100.07 100.07c12.28 12.28 32.2 12.28 44.48 0l22.24-22.24c12.28-12.28 12.28-32.19 0-44.48L242.72 256z" class=""></path></svg></button><input type="hidden" name="attachname[]" value="'+data+'"></div>';
                    
                    $('.uploaded_files').append(html);
                    $('.slider_wrap').css('display','block');
                }
            });
        });
        
    }());   
    
    // ------------------------Post_Comment_Reply Input part------------------------

    (function () {        
        $(document).on('click','.btn_connection',function(){
            
            var id = $(this).data('id');
            
            $.ajax({
                url: "/set_follow",
                method: 'GET', 
                type: 'json',
                data: {id:id},           
                success: function (response) {
                    console.log(response);
                    if(response)
                    {
                        location.reload();
                    }
                }
            });
        });

        $(document).on('click','.btn_like',function(){
            var likes = parseInt($(this).find("span.likes").html());
            if($(this).find('i.fa-heart').hasClass('far'))
            {
                $(this).find("span.likes").html(likes+1);
                $(this).find('i.fa-heart').removeClass('far');
                $(this).find('i.fa-heart').addClass('fas');
            }
            else
            {
                if(likes>0)
                {
                    $(this).find("span.likes").html(likes-1);
                }
                $(this).find('i.fa-heart').removeClass('fas');
                $(this).find('i.fa-heart').addClass('far');
            }
            var post_id = $(this).data('id');
            $.ajax({
                url: "/add_like",
                method: 'GET', 
                type: 'json',
                data: {id:post_id},     
                success: function(result){                  
                    if(result)
                    {
                        
                    }
                }
            })
        });

        $(document).on('click','.btn_like_reply',function(){
            var rid = $(this).data('rid');

            var likes = parseInt($(".cnt_like_reply_"+rid).html());
            if($(this).find('i.fa-heart').hasClass('far'))
            {
                $(this).find("span.likes").html(likes+1);
                $(this).find('i.fa-heart').removeClass('far');
                $(this).find('i.fa-heart').addClass('fas');
            }
            else
            {
                if(likes>0)
                {
                    $(this).find("span.likes").html(likes-1);
                }
                $(this).find('i.fa-heart').removeClass('fas');
                $(this).find('i.fa-heart').addClass('far');
            }
            if(rid=="")
            {
                return false;
            }
            else
            {
                $.ajax({
                    url: "/add_like_reply",
                    method: 'GET', 
                    type: 'json',
                    data: {rid:rid},     
                    success: function(result){                  
                        if(result)
                        {
                            
                        }
                    }
                })
            }
            
        });

        $(document).on('click','.btn_like_comment',function(){
            var likes = parseInt($(this).find("span.likes").html());
            if($(this).find('i.fa-heart').hasClass('far'))
            {
                $(this).find("span.likes").html(likes+1);
                $(this).find('i.fa-heart').removeClass('far');
                $(this).find('i.fa-heart').addClass('fas');
            }
            else
            {
                if(likes>0)
                {
                    $(this).find("span.likes").html(likes-1);
                }
                $(this).find('i.fa-heart').removeClass('fas');
                $(this).find('i.fa-heart').addClass('far');
            }
            var comment_id = $(this).data('cid');
            $.ajax({
                url: "/add_like_comment",
                method: 'GET', 
                type: 'json',
                data: {id:comment_id},     
                success: function(result){                  
                    if(result)
                    {
                        
                    }
                }
            })
        });


        $(document).on('click','.btn_delete_post',function(){
            var id = $(this).data('id');
            if(id == "")
            {
                return false;
            }
            else
            {
                if (!confirm("Do you want to delete")){
                   return false;
                }
                else
                {
                    $.ajax({
                        url: "/delete_post",
                        method: 'GET', 
                        type: 'json',
                        data: {id:id},     
                        success: function(result){                  
                            if(result)
                            {
                                location.reload();
                            }
                        }
                    })
                }
                
            }
            
        });

        $(document).on('click','.attached_item_view',function(){
            var url = $(this).attr('src');           
            $(".wrap_attach_full_view").html("");
            var ext = url.split(".")[1];
            var html='';
            if ($.inArray(ext, imgExtension) == -1) {
                html +=`
                    <video class="modal_view_attach" src="${url}" controls=""></video>
                `;
            }
            else
            {
                html += `
                    <img class="modal_view_attach" src="${url}" controls="">
                `;
            }
            $(".wrap_attach_full_view").append(html);
            $('#viewFullAttach').modal('toggle');
        });

        $(document).on('keyup','#post_content',function(){
            var word_cnt = 0;
            var cnt_remain_txt =  parseInt($(".cnt_remain_txt").html());

            var cur_cnt = $(this).val().length;
            word_cnt = $(this).val().split(" ").length
            if($(this).val()=="")
            {
                word_cnt = 0;
            }
            if(word_cnt >= max_cnt)
            {
                $(".cnt_remain_txt").html('0');
                return false;
            }
            else
            {
                $(".cnt_remain_txt").html(max_cnt-word_cnt);
            }

        });

        $(document).on('click','.btn_show_more_content_comment',function(){
            var comment_id = $(this).data('cid');
            if($(".comment_content_"+comment_id).hasClass('post_text_limit'))
            {
                $(".comment_content_"+comment_id).removeClass('post_text_limit');
                $(".btn_show_more_content_comment").html("less");
            }
            else
            {
                $(".comment_content_"+comment_id).addClass('post_text_limit');
                $(".btn_show_more_content_comment").html("read more");
            }
        });
        $(document).on('click','.btn_show_more_content',function(){
            var post_id = $(this).data('id');
            if($(".post_content_"+post_id).hasClass('post_text_limit'))
            {
                $(".post_content_"+post_id).removeClass('post_text_limit');
                $(".btn_show_more_content").html("less");
            }
            else
            {
                $(".post_content_"+post_id).addClass('post_text_limit');
                $(".btn_show_more_content").html("read more");
            }
        });
        
        $(document).on('click','.btn_hide_post',function(){
            var post_id = $(this).data('id');
            if(post_id == "")
            {
                return false;
            }
            else
            {
                $.ajax({
                    url: "/set_private",
                    method: 'GET', 
                    type: 'json',
                    data: {id:post_id},     
                    success: function(response){                  
                        var result = response.status;
                        if(result == "1")
                        {
                            $(".btn_hide_post_"+post_id).html('<i class="fas fa-times" aria-hidden="true"></i> Hide from public');
                        }
                        else
                        {
                            $(".btn_hide_post_"+post_id).html('<i class="fas fa-times" aria-hidden="true"></i> Show to public');
                            if(where == "dashboardpage")
                            {
                                $(".post_item_"+post_id).remove();
                            }
                        }
                    }
                })
            }
            
        });

        $(document).on('click','.btn_all_replies',function(){
            var cid = $(this).data('id');
            var loopval = 0;
            if($(this).hasClass("expandarea"))
            {
                $(this).removeClass("expandarea");
                $(this).html("All replies");
                $(".added_reply_content_"+cid+" "+".reply_item_"+cid).each(function(){
                    if(loopval > 0)
                    {
                        $(this).addClass("display_none");
                    }
                    loopval +=1;
                });
            }
            else
            {
                $(this).addClass("expandarea");
                $(this).html("Less");                
                                
                $(".added_reply_content_"+cid+" "+".reply_item_"+cid).each(function(){                    
                    $(this).removeClass("display_none");                    
                });
            }
        });

        $(document).on('click','.btn_view_more',function(){
            var pid = $(this).data('pid');
            var loopval = 0;
            if($(this).hasClass("expandarea"))
            {
                $(this).removeClass("expandarea");
                $(this).html("View More Comments");
                $(".added_comment_"+pid+" "+".comment_item_"+pid).each(function(){
                    if(loopval > 0)
                    {
                        $(this).addClass("display_none");
                    }
                    loopval +=1;
                });
            }
            else
            {
                $(this).addClass("expandarea");
                $(this).html("Less");                
                $(".added_comment_"+pid+" "+".comment_item_"+pid).each(function(){
                    if(loopval > 0)
                    {
                        $(this).removeClass("display_none");
                    }
                    loopval +=1;
                });
            }
        });


        $(document).on('click','.btn_autocomment',function(){
            var post_id = $(this).data('pid');
            var comment = $(this).data('text');            
            if(comment == "")
            {
                return false;
            }
            else
            {        
                
                var cnt_comment = parseInt($(".cnt_comment_"+post_id).html());    
                $(".cnt_comment_"+post_id).html(cnt_comment+1);   
                $.ajax({
                    url: "/addcomment",
                    method: 'GET',  
                    type: 'json',
                    data: {post_id:post_id,content:comment},          
                    success: function (response) {
                        if(response.results)
                        {
                            
                            var html = `
                            <div class="p-3 d-flex comment_item_${response.pid} comment_num_${response.cid}  w-100">
                                    <div class="dropdown-list-image mr-1 ml-2">
                                        <img class="rounded-circle" src="${cur_user_avatar_url}"> 
                                    </div>
                                    <div class="w-100">
                                    <div class="comment_text pos_rel">
                                        <div>
                                            <div class="dropdown pos_rel">
                                                <label class="user_name_style_ofComment">
                                                    ${cur_user_full_name}
                                                </label>
                                                <p class="timestyle_created">
                                                    1Min ago
                                                </p>
                                                <button class="btn btn_dropdown" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                                            <i class="fas fa-ellipsis-h" aria-hidden="true"></i>
                                                        </button>
                                                <div class="dropdown-menu dropdown_custom_position" style=""> 
                                                    <button class="btn_transparent dropdown-item btn_edit_comment" data-cid="${response.cid}" data-pid="${response.pid}" data-toggle="modal" data-target="#editCommentModal">
                                                        <i class="far fa-edit" aria-hidden="true"></i> Edit
                                                    </button>
                                                    <button class="btn_transparent dropdown-item btn_delete_comment" data-cid="${response.cid}" data-pid="${response.pid}">
                                                        <i class="far fa-trash-alt" aria-hidden="true"></i> Delete
                                                    </button>                                                           
                                                </div>
                                            </div>                                            
                                        </div>
                                                                                              
                                        <div class="pt-10">
                                            <p class="comment_content_${response.cid}">
                                                ${comment}
                                            </p>
                                        </div>                 
                                        </div>
                                    
                                    <div class="py-1">
                                        <button class="mr-2 btn_transparent btn_cnt_style btn_like_comment" data-cid="${response.cid}">
                                            <i class="far fa-heart text-warning display_none" aria-hidden="true"></i>  
                                            &nbsp;Like(<span class="cnt_number_style likes">0</span>)</button>
                                        <button class="mr-2 btn_transparent btn_cnt_style btn_viewreply" data-id="${response.cid}"><i class="fas fa-reply display_none"></i>&nbsp;Reply(<span class="cnt_number_style cnt_reply_${response.cid}">0</span>)</button>                                       
                                    </div>
                                    <div class="display_closed added_reply_${response.cid}">
                                        <div class="p-3 d-flex align-items-center w-100">
                                            <div class="dropdown-list-image ml-2 mr-1">
                                                <img class="rounded-circle" src="${cur_user_avatar_url}"> 
                                            </div>
                                            <div class="w-100 pos_rel pl-2">
                                                <textarea placeholder="Write a reply" class="form-control border-0 p-0 shadow-none reply_content_txt_${response.cid}" name="content" rows="2"></textarea>
                                                <button type="button" class="btn_store_reply" data-cid="${response.cid}">
                                                    <i class="fas fa-reply" aria-hidden="true"></i>
                                                </button>
                                            </div>
                                        </div>
                                        <div class="added_reply_content_${response.cid}">

                                        </div>
                                        <div class="text-right added_reply_action_${response.cid}">
                                            <button class="btn_transparent display_none btn_all_replies btn_all_replies_${response.cid}" data-id="${response.cid}">All replies
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>                                
                                `;      

                            $(".added_comment_"+post_id).prepend(html);
                        }
                        else
                        {
                            location.reload();
                        }
                    }   
                });         

               
            }
        });

        $(document).on('click','.btn_delete_reply',function(){
            var  rid = $(this).data('rid');
            var  comment_id = $(this).data('cid');
            if(rid == "")
            {
                return false;
            }
            else
            {         
                $("#reply_item_"+rid).remove();      

                var loopval = 0;
                $(".added_reply_content_"+comment_id+" "+".reply_item_"+comment_id).each(function(){                    
                    loopval +=1;
                   
                });
                if(loopval < 2)
                {
                    if($(".btn_all_replies_"+comment_id).hasClass("expandarea"))
                    {
                        $(".btn_all_replies_"+comment_id).removeClass("expandarea");
                        $(".btn_all_replies_"+comment_id).addClass("display_none");
                    }
                }
                var cnt_reply = parseInt($(".cnt_reply_"+comment_id).html());
                if(cnt_reply > 0)
                {
                    $(".cnt_reply_"+comment_id).html(cnt_reply-1);
                }
                $.ajax({
                    url: "/deletereply",
                    method: 'GET',  
                    type: 'json',
                    data: {rid:rid},          
                    success: function (response) {
                        if(!response.results)
                        {
                            // location.reload();
                        }
                    }            
                });
            }
        
        
        });

        $(document).on('click','.btn_delete_comment',function(){
            var  cid = $(this).data('cid');
            var  post_id = $(this).data('pid');
            if(cid == "")
            {
                return false;
            }
            else
            {
                $(".comment_num_"+cid).remove();
                var cnt_comment = parseInt($(".cnt_comment_"+post_id).html());
                if(cnt_comment > 0)
                {
                    $(".cnt_comment_"+post_id).html(cnt_comment-1);
                }
                $.ajax({
                    url: "/deletecomment",
                    method: 'GET',  
                    type: 'json',
                    data: {cid:cid},          
                    success: function (response) {
                        if(!response.results)
                        {
                            location.reload();
                        }
                    }            
                });
            }
        
        
        });

        $(document).on('click','.btn_store_reply',function(){
            var comment_id = $(this).data('cid');
            var reply = $(".reply_content_txt_"+comment_id).val();            
            var cnt_reply = parseInt($(".cnt_reply_"+comment_id).html());            
            if(reply == "")
            {
                return false;
            }
            else
            {
                $(".reply_content_txt_"+comment_id).val(''); 
                $(".cnt_reply_"+comment_id).html(cnt_reply+1);            
                $.ajax({
                    url: "/addreply",
                    method: 'GET',  
                    type: 'json',
                    data: {comment_id:comment_id,content:reply},          
                    success: function (response) {
                        if(response.results)
                        {
                            var html = `
                                <div class="p-3 reply_item_${response.cid} d-flex align-items-center w-100">
                                    <div class="dropdown-list-image mr-1 ml-2">
                                        <img class="rounded-circle" src="${cur_user_avatar_url}"> 
                                    </div>
                                    <div class="w-100 comment_text pos_rel">
                                        <p>
                                            ${reply}
                                        </p>                              
                                        <button type="button" class="btn_delete_reply btn_transparent btn_delete_effect" data-cid="${response.rid}" data-pid="${response.cid}">
                                                <i class="fas fa-times" aria-hidden="true"></i>
                                        </button>
                                    </div>
                                </div>`;        

                                var html = `
                                <div class="p-3 reply_item_${response.cid} d-flex align-items-center w-100">
                                    <div class="dropdown-list-image mr-1 ml-2">
                                        <img class="rounded-circle" src="${cur_user_avatar_url}"> 
                                    </div>
                                    <div class="w-100 comment_text pos_rel">
                                        <div>                                                   
                                            <div class="dropdown pos_rel">
                                                <label class="user_name_style_ofComment">
                                                    ${cur_user_full_name}
                                                </label>
                                                <p class="timestyle_created">
                                                    1Min ago
                                                </p>
                                                <button class="btn btn_dropdown" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                                    <i class="fas fa-ellipsis-h" aria-hidden="true"></i>
                                                </button>
                                                <div class="dropdown-menu dropdown_custom_position" style=""> 
                                                    <button class="btn_transparent dropdown-item btn_edit_comment" data-cid="57" data-pid="13" data-toggle="modal" data-target="#editCommentModal">
                                                        <i class="far fa-edit" aria-hidden="true"></i> Edit
                                                    </button>
                                                    <button class="btn_transparent dropdown-item btn_delete_reply" data-rid="${response.rid}" data-cid="${response.cid}">
                                                        <i class="far fa-trash-alt" aria-hidden="true"></i> Delete
                                                    </button>                                                           
                                                </div>
                                            </div>                                            
                                        </div>
                                        <div class="pt-10">
                                            <p class="reply_content reply_content_${response.rid}">
                                                ${reply}
                                            </p>
                                            <button class="mt-2 btn_transparent btn_like_reply" data-rid="${response.rid}">
                                                <i class="far fa-heart text-danger" aria-hidden="true"></i>                                                
                                                <span>( </span><span class="likes cnt_like_reply cnt_number_style cnt_like_reply_${response.rid}">0
                                                </span><span> )</span>
                                            </button>                                                    
                                        </div>
                                    </div>
                                </div>`;  
                            $(".added_reply_content_"+comment_id).prepend(html);
                        }
                        else
                        {
                            location.reload();
                        }
                    }   
                });         

               
            }
        });


        $(document).on('click','.btn_viewreply',function(){
            var comment_id = $(this).data('id');
            
            if($(".added_reply_"+comment_id).hasClass('display_closed'))
            {                
                $(".added_reply_"+comment_id).removeClass('display_closed');
                $(".added_reply_"+comment_id).slideDown("slow");
                if(comment_id =="")
                {
                    return false;
                }
                else
                {
                    $.ajax({
                        url: "/getreplies",
                        method: 'GET',  
                        type: 'json',
                        data: {cid:comment_id},          
                        success: function (response) {                            
                            var data = response.replies;
                            
                            if(data.length>0)
                            {
                                $(".added_reply_content_"+comment_id).html("");
                                for(var i=0;i<data.length;i++)
                                {
                                    var html = `
                                        <div id="reply_item_${data[i].rid}" class="p-3 reply_item_${data[i].cid} d-flex w-100">
                                            <div class="dropdown-list-image comment_user_avatar_margin">
                                                <img class="rounded-circle" src="`;
                                            if(data[i].avatar=="")
                                            {
                                                html+="/static/img/user.png";
                                            }
                                            else
                                            {
                                                html+=data[i].avatar;
                                            }
                                        html+=`"> 
                                            </div>
                                            <div class="w-100 comment_text pos_rel">
                                                <div>                                                   
                                                    <div class="dropdown pos_rel">
                                                        <label class="user_name_style_ofComment">
                                                            ${data[i].full_name}
                                                        </label>
                                                        <p class="timestyle_created">
                                                            ${data[i].created_at} ago
                                                        </p>
                                                        `;
                                                    if(data[i].me == "1")
                                                    {
                                                    html +=`
                                                        <button class="btn btn_dropdown" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                                            <i class="fas fa-ellipsis-h" aria-hidden="true"></i>
                                                        </button>
                                                        <div class="dropdown-menu dropdown_custom_position" style=""> 
                                                            <button class="btn_transparent dropdown-item btn_edit_reply" data-rid="${data[i].rid}" data-toggle="modal" data-target="#editReplyModal">
                                                                <i class="far fa-edit" aria-hidden="true"></i> Edit
                                                            </button>
                                                            <button class="btn_transparent dropdown-item btn_delete_reply" data-rid="${data[i].rid}" data-cid="${data[i].cid}">
                                                                <i class="far fa-trash-alt" aria-hidden="true"></i> Delete
                                                            </button>                                                           
                                                        </div>`;
                                                    }
                                                    html +=`
                                                    </div>                                                    
                                                </div>
                                                <div class="pt-10">
                                                    <p class="reply_content reply_content_${data[i].rid}">
                                                        ${data[i].content}
                                                    </p>
                                                    <button class="mt-2 btn_transparent btn_like_reply" data-rid="${data[i].rid}">`;
                                                    if(data[i].mylike == "1")
                                                    {
                                                        html+=`
                                                        <i class="fas fa-heart text-danger" aria-hidden="true"></i>
                                                        `;
                                                    }
                                                    else
                                                    {
                                                        html+=`
                                                        <i class="far fa-heart text-danger" aria-hidden="true"></i>
                                                        `;
                                                    }  
                                                html+=`
                                                        <span>( </span>
                                                        <span class="likes cnt_number_style cnt_like_reply cnt_like_reply_${data[i].rid}">${data[i].likes}
                                                        </span>
                                                        <span> )</span>
                                                    </button>                                                    
                                                </div>
                                            </div>
                                        </div>`;        
                                    $(".added_reply_content_"+comment_id).append(html);
                                }
                                if(data.length>1)
                                {                                    
                                    var cid = data[0].cid;
                                    if($(".btn_all_replies_"+cid).hasClass('display_none'))
                                    {
                                        $(".btn_all_replies_"+cid).removeClass('display_none');
                                    }
                                    if($(".btn_all_replies_"+cid).hasClass("expandarea"))
                                    {
                                        $(".btn_all_replies_"+cid).removeClass("expandarea");
                                        $(".btn_all_replies_"+cid).html("All replies");
                                    }

                                    var loopval = 0;
                                    $(".added_reply_content_"+cid+" "+".reply_item_"+cid).each(function(){
                                        if(loopval > 0)
                                        {
                                            $(this).addClass("display_none");
                                        }
                                        loopval +=1;
                                    });
                                }
                                
                            }
                        }            
                    });
                }
            }
            else
            {               
                $(".added_reply_"+comment_id).addClass('display_closed');
                $(".added_reply_"+comment_id).slideUp(("slow"));
            }
            
        });

        $(document).on('click','.btn_store_comment',function(){
            var post_id = $(this).data('pid');
            var comment = $(".comment_content_txt_"+post_id).val();
            var cnt_comment = parseInt($(".cnt_comment_"+post_id).html());
            if(comment == "")
            {
                return false;
            }
            else
            {
                $(".comment_content_txt_"+post_id).val(''); 
                $(".cnt_comment_"+post_id).html(cnt_comment+1);            
                $(".total_cnt_comments_"+post_id).html("1 of "+(cnt_comment+1));            
                $.ajax({
                    url: "/addcomment",
                    method: 'GET',  
                    type: 'json',
                    data: {post_id:post_id,content:comment},          
                    success: function (response) {
                        if(response.results)
                        {
                           
                            var html = `
                                <div class="p-3 d-flex comment_item_${response.pid} comment_num_${response.cid}  w-100">
                                    <div class="dropdown-list-image mr-1 ml-2">
                                        <img class="rounded-circle" src="${cur_user_avatar_url}"> 
                                    </div>
                                    <div class="w-100">
                                    <div class="comment_text pos_rel">
                                        <div>
                                            <div class="dropdown pos_rel">
                                                <label class="user_name_style_ofComment">
                                                    ${cur_user_full_name}
                                                </label>
                                                <p class="timestyle_created">
                                                    1Min ago
                                                </p>
                                                <button class="btn btn_dropdown" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                                            <i class="fas fa-ellipsis-h" aria-hidden="true"></i>
                                                        </button>
                                                <div class="dropdown-menu dropdown_custom_position" style=""> 
                                                    <button class="btn_transparent dropdown-item btn_edit_comment" data-cid="${response.cid}" data-pid="${response.pid}" data-toggle="modal" data-target="#editCommentModal">
                                                        <i class="far fa-edit" aria-hidden="true"></i> Edit
                                                    </button>
                                                    <button class="btn_transparent dropdown-item btn_delete_comment" data-cid="${response.cid}" data-pid="${response.pid}">
                                                        <i class="far fa-trash-alt" aria-hidden="true"></i> Delete
                                                    </button>                                                           
                                                </div>
                                            </div>                                            
                                        </div>
                                                                                              
                                        <div class="pt-10">
                                            <p class="comment_content comment_content_${response.cid}">
                                                ${comment}
                                            </p>
                                        </div>                 
                                        </div>
                                    
                                    <div class="py-1">
                                        <button class="mr-2 btn_transparent btn_cnt_style btn_like_comment" data-cid="${response.cid}">
                                            <i class="far fa-heart text-warning display_none" aria-hidden="true"></i>  
                                            &nbsp;Like(<span class="cnt_number_style likes">0</span>)</button>
                                        <button class="mr-2 btn_transparent btn_cnt_style btn_viewreply" data-id="${response.cid}"><i class="fas fa-reply display_none"></i>&nbsp;Reply(<span class="cnt_number_style cnt_reply_${response.cid}">0</span>)</button>                                       
                                    </div>
                                    <div class="display_closed added_reply_${response.cid}">
                                        <div class="p-3 d-flex align-items-center w-100">
                                            <div class="dropdown-list-image mr-3">
                                                <img class="rounded-circle" src="${cur_user_avatar_url}"> 
                                            </div>
                                            <div class="w-100 pos_rel">
                                                <textarea placeholder="Write a reply" class="form-control shadow-none reply_content_txt_${response.cid}" name="content" rows="2"></textarea>
                                                <button type="button" class="btn_store_reply" data-cid="${response.cid}">
                                                    <i class="fas fa-reply" aria-hidden="true"></i>
                                                </button>
                                            </div>
                                        </div>
                                        <div class="added_reply_content_${response.cid}">

                                        </div>
                                        <div class="text-right added_reply_action_${response.cid}">
                                            <button class="btn_transparent display_none btn_all_replies btn_all_replies_${response.cid}" data-id="${response.cid}">All replies
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>`;        
                            $(".added_comment_"+post_id).prepend(html);
                        }
                        else
                        {
                            location.reload();
                        }
                    }   
                });         

               
            }
        });
        
        $(document).on('click','.btn_viewcomment',function(){
            var post_id = $(this).data('id');
            if($(".comment_content_"+post_id).hasClass('display_closed'))
            {
                $(".comment_content_"+post_id).removeClass('display_closed');
                $(".comment_content_"+post_id).slideDown("slow");
                if(post_id =="")
                {
                    return false;
                }
                else
                {
                    $.ajax({
                        url: "/getcomments",
                        method: 'GET',  
                        type: 'json',
                        data: {pid:post_id},          
                        success: function (response) {                            
                            var data = response.comments;
                            
                            if(data.length>0)
                            {
                                $(".added_comment_"+post_id).html("");
                                for(var i=0;i<data.length;i++)
                                {
                                    var html = `
                                        <div class="p-3 d-flex comment_item_${data[i].pid} comment_num_${data[i].cid} w-100">
                                            <div class="dropdown-list-image comment_user_avatar_margin">
                                                <img class="rounded-circle" src="`;
                                        if(data[i].avatar=="")
                                        {
                                            html +="/static/img/user.png";
                                        }
                                        else
                                        {
                                            html +=data[i].avatar;
                                        }                                        
                                            html +=`"> 
                                            </div>
                                            <div class="w-100">
                                            <div class="comment_text pos_rel">
                                                <div>                                                   
                                                    <div class="dropdown pos_rel">
                                                        <label class="user_name_style_ofComment">
                                                            ${data[i].full_name}
                                                        </label>
                                                        <p class="timestyle_created">
                                                            ${data[i].created_at} ago
                                                        </p>
                                                        `;
                                                if(data[i].me=='1')
                                                {
                                                html += `<button class="btn btn_dropdown" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                                            <i class="fas fa-ellipsis-h" aria-hidden="true"></i>
                                                        </button>
                                                        <div class="dropdown-menu dropdown_custom_position" style=""> 
                                                            <button class="btn_transparent dropdown-item btn_edit_comment" data-cid="${data[i].cid}" data-pid="${data[i].pid}" data-toggle="modal" data-target="#editCommentModal">
                                                                <i class="far fa-edit" aria-hidden="true"></i> Edit
                                                            </button>
                                                            <button class="btn_transparent dropdown-item btn_delete_comment" data-cid="${data[i].cid}" data-pid="${data[i].pid}">
                                                                <i class="far fa-trash-alt" aria-hidden="true"></i> Delete
                                                            </button>                                                           
                                                        </div>`;
                                                }
                                                html += `</div>                                                    
                                                </div>
                                                <div class="pt-10">
                                                    <span class="comment_content post_text_limit comment_content_${data[i].cid}">
                                                        ${data[i].content}
                                                    </span>`;
                                                if(data[i].content.length>250)
                                                {
                                                    html +=`<button class="btn_transparent btn_show_more_content_comment" data-cid="${data[i].cid}">
                                                        read more
                                                    </button>`;    
                                                }
                                                

                                            html +=`
                                                    </div>                                                                                           
                                                </div>
                                            
                                            <div class="py-1">
                                                <button class="mr-2 btn_transparent btn_cnt_style btn_like_comment" data-cid="${data[i].cid}">
                                                    `;
                                            if(data[i].mylike=="1")
                                            {
                                                html+=`<i class="fas fa-heart display_none text-warning" aria-hidden="true"></i>`;
                                            }
                                            else
                                            {
                                                html+=`<i class="far fa-heart display_none text-warning" aria-hidden="true"></i>`;
                                            }
                                            html +=`                                                    
                                                    &nbsp;Like(<span class="likes cnt_number_style">${data[i].likes}</span>)</button>
                                                <button class="mr-2 btn_cnt_style btn_transparent btn_viewreply" data-id="${data[i].cid}"><i class="fas fa-reply display_none"></i>&nbsp;Reply(<span class="cnt_number_style cnt_reply_${data[i].cid}">${data[i].replies}</span>)</button>
                                                
                                            </div>
                                            <div class="display_closed added_reply_${data[i].cid}">
                                                
                                                <div class="added_reply_content_${data[i].cid}">

                                                </div>
                                                <div class="text-right added_reply_action_${data[i].cid}">
                                                    <button class="btn_transparent display_none btn_all_replies btn_all_replies_${data[i].cid}" data-id="${data[i].cid}">All replies
                                                    </button>
                                                </div>
                                                <div class="p-3 d-flex align-items-center w-100">
                                                    <div class="dropdown-list-image ml-2 mr-1">
                                                        <img class="rounded-circle" src="${cur_user_avatar_url}"> 
                                                    </div>
                                                    <div class="w-100 pos_rel pl-2">
                                                        <textarea placeholder="Write a reply" class="form-control shadow-none reply_content_txt reply_content_txt_${data[i].cid}" name="content" rows="1"></textarea>
                                                        <button type="button" class="btn_store_reply" data-cid="${data[i].cid}">
                                                            <i class="fas fa-reply" aria-hidden="true"></i>
                                                        </button>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>`;        
                                    $(".added_comment_"+post_id).append(html);
                                }
                                if(data.length>1)
                                {
                                    var pid = data[0].pid;
                                    if($(".btn_view_more_"+pid).hasClass('display_none'))
                                    {
                                        $(".btn_view_more_"+pid).removeClass('display_none');
                                    }
                                    if($(".btn_view_more_"+pid).hasClass("expandarea"))
                                    {
                                        $(".btn_view_more_"+pid).removeClass("expandarea");
                                        $(".btn_view_more_"+pid).html("View More Comments");
                                    }

                                    var loopval = 0;
                                    $(".added_comment_"+pid+" "+".comment_item_"+pid).each(function(){
                                        if(loopval > 0)
                                        {
                                            $(this).addClass("display_none");
                                        }
                                        loopval +=1;
                                    });
                                    $(".total_cnt_comments_"+pid).html("1 of "+data.length);
                                }
                                
                            }
                        }            
                    });
                }
            }
            else
            {
                $(".comment_content_"+post_id).addClass('display_closed');
                $(".comment_content_"+post_id).slideUp(("slow"));
            }
            
        });
           
        $(document).on('click','.btn_cancel_update_post',function(){
            $(".post_content").val('');
            $("#post_id").val('');
            $(".slider_wrap").css("display",'none');
            $('.uploaded_files').html("");   
            $('.btn_cancel_update_post').remove();
            $(".btn_store_post").html("Submit");
        });

        $(document).on('click','.btn_update_reply',function(){
            
            var rid = $("#editReplyID").val();
            var content = $("#editReplyModalContent").val();
            if(rid=="")
            {
                return false;
            }
            if(content=="")
            {
                return false;
            }
            
            $.ajax({
                url: "/updatereply",
                method: 'GET',  
                type: 'json',
                data: {rid:rid,content:content},          
                success: function (response)
                {  
                    $(".reply_content_"+rid).html(content);
                    $("#editReplyModal").modal('toggle');
                }   
            });  
            
        });
        
        $(document).on('click','.btn_update_comment',function(){
            
            var cid = $("#editCommentID").val();
            var content = $("#editCommentContent").val();
            if(cid=="")
            {
                return false;
            }
            if(content=="")
            {
                return false;
            }
            
            $.ajax({
                url: "/updatecomment",
                method: 'GET',  
                type: 'json',
                data: {cid:cid,content:content},          
                success: function (response)
                {  
                    $(".comment_content_"+cid).html(content);
                    $("#editCommentModal").modal('toggle');
                }   
            });  
            
        });

        $(document).on('click','.btn_edit_reply',function(){
            var rid = $(this).data('rid');
                
            $("#editReplyID").val(rid);

            
            $.ajax({
                url: "/getreply",
                method: 'GET',  
                type: 'json',
                data: {rid:rid},          
                success: function (response)
                {  
                    $("#editReplyModalContent").val(response.data);
                }   
            });  
            
        });
        
        $(document).on('click','.btn_edit_comment',function(){
            var pid = $(this).data('pid');
            var cid = $(this).data('cid');    
            $("#editCommentID").val(cid);

            
            $.ajax({
                url: "/getcomment",
                method: 'GET',  
                type: 'json',
                data: {cid:cid},          
                success: function (response)
                {  
                    $("#editCommentContent").val(response.data);
                }   
            });  
            
        });

        $(document).on('click','.btn_edit_post',function(){
            var id = $(this).data('id');
            $.ajax({                
                url:"/get_selected_post",
                type: 'get',
                dataType: 'json',
                data: {id:id},

                success: function(result){       
                    var data = result.results;           
                    if(data.post_id != "")
                    {
                        $("html, body").animate({ scrollTop: 0 }, "slow");
                        var content = data.content;
                        var post_id = data.post_id;
                        var attachs = data.attach;
                        var visibleto = data.visibleto;
                        
                        $('.select_public option[value="'+visibleto+'"]').attr('selected','selected');
                        $(".post_content").val(content);
                        $("#post_id").val(post_id);
                        $(".btn_store_post").html("Update post");
                        
                        var btn_cancel = $("body").find(".btn_cancel_update_post");
                        if(btn_cancel.length < 1)
                        {
                            var cancelhtml = `
                                <button type="button" class="btn btn-sm btn_cancel_update_post">Cancel</button>
                            `;
                        }                        

                        $(".add_cancel_btn").prepend(cancelhtml);
                        
                        if(attachs.length > 0)
                        {
                            $(".slider_wrap").css("display",'block');
                            $('.uploaded_files').html("");                                                      
                            for(var j=0;j<attachs.length;j++)                            {                               
                                
                                var data = attachs[j]; 
                                var fileExt = data.split(".")[1];
                                
                                let html = '<div class="uploaded_files_item">';
                                if ($.inArray(fileExt, imgExtension) == -1) {
                                    html += '<video src="/media/'+data+'" controls></video>';
                                }
                                else
                                {
                                    html += '<img src="/media/'+data+'" alt="">';
                                }
                                html += '<button class="btn_transparent btn_delete_uploadedFile"><svg style="width:15px;height:15px;" aria-hidden="true" focusable="false" data-prefix="fas" data-icon="times" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 352 512" class="svg-inline--fa fa-times fa-w-11 fa-3x"><path fill="currentColor" d="M242.72 256l100.07-100.07c12.28-12.28 12.28-32.19 0-44.48l-22.24-22.24c-12.28-12.28-32.19-12.28-44.48 0L176 189.28 75.93 89.21c-12.28-12.28-32.19-12.28-44.48 0L9.21 111.45c-12.28 12.28-12.28 32.19 0 44.48L109.28 256 9.21 356.07c-12.28 12.28-12.28 32.19 0 44.48l22.24 22.24c12.28 12.28 32.2 12.28 44.48 0L176 322.72l100.07 100.07c12.28 12.28 32.2 12.28 44.48 0l22.24-22.24c12.28-12.28 12.28-32.19 0-44.48L242.72 256z" class=""></path></svg></button><input type="hidden" name="attachname[]" value="'+data+'"></div>';
                                
                                $('.uploaded_files').append(html);
                            }                            
                        }  
                    }
                    else
                    {
                        location.reload();
                    }
                }
            }); 
        });

        $(".btn_store_post").click(function(){
            var content = $(".post_content").val();
            if(content == "")
            {                
                var uploadedfiles = 0;
                $(".uploaded_files_item").each(function(){
                    uploadedfiles +=1;
                });
                if(uploadedfiles < 1)
                {
                    return false;
                }
            }
            var data = $("#form_create_post").serialize();           
            
            $("#loading").css("display","block");
            $.ajax({                
                url:"/store_post",
                type: 'post',
                dataType: 'json',
                data: data,

                success: function(result){                  
                    location.reload();
                }
            }); 
        });

        $(document).on('click','.btn_delete_uploadedFile',function(){
            $(this).parent().remove();
            var cur_file_number = 0; 
            $(".uploaded_files_item").each(function(){
                cur_file_number++;
            })
            if(cur_file_number==0)
            {
                $('.slider_wrap').css('display','none');
            }
        });

    }());   
   
   

});


    

