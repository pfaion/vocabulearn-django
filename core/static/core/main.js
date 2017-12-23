var active_item = null;
var set_id = null;

$(document).ready(function() {
  add_list_click_handlers();
  add_detail_focusout_save_handlers();
  add_tab_navigation();
  reload_list_numbering();
  
  select_list_item($("#flashcard-list").find(".row").first());
  $("#detail-front").focus();
  
  
  $(".delete-card-button").hover(function(){
    $(this).toggleClass("bg-danger");
    $(this).toggleClass("text-white");
  });
  
  $("#set-list").find(".folder-add .row, .card-set-add .row").hover(function(){
    $(this).toggleClass("alert-success");
    $(this).toggleClass("text-secondary");
  });
  
  $("#set-list").find(".folder").click(function(){
    $(this).find(".icon span").each(function() {
      $(this).toggleClass("hidden");
    });
    $(this).nextAll().each(function() {
      if($(this).hasClass("folder") || $(this).hasClass("folder-add")) {
        return false;
      } else {
        $(this).toggleClass("hidden");
      }
    });
  });
  
  $("#set-list").find(".card-set .row").hover(function() {
    $(this).toggleClass("alert-secondary");
  });
  
  
  
  $("#set-list").find(".folder-add .row").click(function() {
    console.log("clicked add folder");
    setup_modal("Add Folder");
    set_modal_submit(submit_add_folder);
    show_modal();
  });
  
  
  
  
  $("#set-list").find(".card-set-add .row").click(function() {
    var folder_id = $(this).find(".folder-id").html();
    setup_modal("Add Card Set");
    set_modal_submit(submit_add_set, folder_id);
    show_modal();
  });
  
  
  set_id = $("#set-id").html()
  
});

function submit_add_folder() {
  console.log("submit add folder called");
  $.ajax({
    method: "PUT",
    url: `/API/folder/new/`,
  }).done(function(data) {
    console.log("created done");
    var id = data.id;
    var name = $("#modal").find("#field").val();
    $.ajax({
      method: "POST",
      url: `/API/folder/${id}/`,
      data: {
        name: name
      }
    }).done(function() {
      console.log("updated done");
      location.reload();
    });
  });
}

function submit_add_set(folder_id) {
  console.log("submit add set called");
  $.ajax({
    method: "PUT",
    url: `/API/set/new/${folder_id}/`,
  }).done(function(data) {
    console.log("created done");
    var id = data.id;
    var name = $("#modal").find("#field").val();
    $.ajax({
      method: "POST",
      url: `/API/set/${id}/`,
      data: {
        name: name
      }
    }).done(function() {
      console.log("updated done");
      window.location.replace(`/set/${id}/`);
    });
  });
}

function setup_modal(title) {
  var button_text = title.split(" ")[0];
  $("#modal").find(".modal-title").html(title);
  $("#modal").find("#submit-button").html(button_text);
  
  $("#modal").find("#submit-button").off("click");
  $("#modal").find("form").off("submit");
}

function set_modal_submit(callback, data=null) {
  $("#modal").find("#submit-button").click(function() {
    callback(data);
  });
  $("#modal").find("form").submit(function(event) {
    event.preventDefault();
    callback(data);
  });
}

function show_modal() {
  $("#modal").modal("show");
  $("#modal").find("#field").focus();
}


function add_list_click_handlers() {
  $("#flashcard-list").find(".row").each(function() {
    $(this).click(list_click_handler);
    add_delete_button_handler(this);
    
  });
  
}

function list_click_handler() {
  select_list_item(this);
  $("#detail-front").focus();
}

function select_list_item(item) {
  set_item_active(item);
  show_item_detail(item);
  if($(active_item).prevAll().length < 4) {
    $(document).scrollTop(0);
  } else {
    $(active_item).prevAll()[3].scrollIntoView();
  }
  // $(document).scrollTop($(document).scrollTop() - 200);
}

function set_item_active(item) {
  if(active_item) $(active_item).removeClass("list-group-item-primary");
  $(item).addClass("list-group-item-primary");
  active_item = item;
}

function show_item_detail(item) {
  ["front", "back"].forEach(function(type) {
    var content = $(item).children(`.${type}`).html();
    var field = $(`#detail-${type}`);
    field.val(content);
  })
}

function add_delete_button_handler(list_item) {
  var id = $(list_item).find('span.id').html();
  $(list_item).find('.delete-card-button').click(function(event) {
    event.stopPropagation();
    delete_card(id);
    $(list_item).addClass('bg-danger');
  })
}

function delete_card(id) {
  if($(active_item).find('.id').html() == id) {
    var next = $(active_item).next()
    if(next.length) {
      select_list_item(next);
    } else {
      var prev = $(active_item).prev()
      select_list_item(prev);
    }
  }
  $.ajax({
    method: "DELETE",
    url: `/API/card/delete/${id}/`,
  }).done(function() {
    $(`#card-${id}`).remove();
    reload_list_numbering();
  });
}

function add_detail_focusout_save_handlers() {
  $("#detail-front").focusout(check_flashcard_change);
  $("#detail-back").focusout(check_flashcard_change);
}

function check_flashcard_change() {
  var active_card_id = $(active_item).children(".id").html();
  var changed_front = $("#detail-front").val();
  var changed_back = $("#detail-back").val();
  var list_item = $(`#card-${active_card_id}`);
  var old_front = list_item.children(".front").html();
  var old_back = list_item.children(".back").html();
  
  if(changed_front != old_front || changed_back != old_back) {
    card = {
      id: active_card_id,
      front: changed_front,
      back: changed_back,
    }
    save_flashcard(card);
  }
}

function save_flashcard(card) {
  var item = $(active_item);
  $.ajax({
    method: "POST",
    url: `/API/card/${card.id}/`,
    data: {
      front: card.front,
      back: card.back,
    }
  }).done(function() {
    reload_list_item(card.id).done(function(){
      $(item).addClass("bg-success");
      setTimeout(function() {
        $(item).removeClass("bg-success");
      }, 500);
    });
  }).fail(function() {
    alert("Fail.");
  });
}

function reload_list_item(id) {
  return $.ajax({
    method: "GET",
    url: `/API/card/${id}/`
  }).done(function(data) {
    var list_item = $(`#card-${id}`);
    list_item.find(".front").html(data.front);
    list_item.find(".back").html(data.back);
    list_item.find(".front_short").html(data.front);
    list_item.find(".back_short").html(data.back);
  });
}

function add_tab_navigation() {
  $("#detail-front").keydown(function(event) {
    if(event.keyCode == 9) {
      event.preventDefault();
      if(event.shiftKey) {
        var prev = $(active_item).prev();
        if(prev.length) {
          $("#detail-back").focus();
          select_list_item(prev);
        } else {
          return;
        }
      } else {
        $("#detail-back").focus();
      }
    }
  });
  $("#detail-back").keydown(function(event) {
    if(event.keyCode == 9) {
      event.preventDefault();
      if(event.shiftKey) {
        $("#detail-front").focus();
      } else {
        var next = $(active_item).next();
        if(next.length) {
          $("#detail-front").focus();
          select_list_item(next);
        } else {
          extend_cards();
          return;
        }
      }
    }
  });
}

function extend_cards() {
  console.log("extend");
  var current_active = active_item;
  $.ajax({
    method: "PUT",
    url: `/API/card/new/${set_id}/`,
  }).done(function(data) {
    var new_list_item = $(current_active).clone();
    new_list_item.prop("id", `card-${data.id}`);
    new_list_item.find(".id").html(data.id)
    new_list_item.find(".front_short").html(data.front)
    new_list_item.find(".back_short").html(data.back)
    new_list_item.find(".front").html(data.front)
    new_list_item.find(".back").html(data.back)
    new_list_item.click(list_click_handler);
    add_delete_button_handler(new_list_item);
    new_list_item.insertAfter($(current_active));
    $("#detail-front").focus();
    select_list_item(new_list_item);
    reload_list_numbering();
  });
}

function reload_list_numbering() {
  $('#flashcard-list').find(".row").each(function(index, list_item) {
    $(list_item).find('.list-number').html(index + 1);
  });
  $("#card-count").html($('#flashcard-list').find(".row").length);
}


