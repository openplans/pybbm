function pybb_delete_post(url, post_id, confirm_text){
    conf = confirm(confirm_text);
    if (!conf) return false;
    obj = {url: url,
        type: 'POST',
        dataType: 'text',
        success: function (data, textStatus) {
            if (data.length > 0) {
                window.location = data;
            } else {
                $("#" + post_id).slideUp();
            }
        }
    };
    $.ajax(obj);
}

$(function() {
    // This is logic for handling subscription requests asynchonously
    // TODO: this only works for the topic list. Update to work on the topic
    // page and the watch area subscriptions.
    $('a.subscription-toggle').click(function(evt) {
        evt.preventDefault();
        var $link = $(this),
            url = $link.attr('href');

        // Submit the request
        $.post(url, function(data, textStatus, jqXHR){
            // Update the href and label
            if($link.hasClass('add-subscription')) {
                $link.text($link.attr('data-delete-subscription-label'));
                $link.attr('href', $link.attr('data-delete-subscription-href'));
            } else {
                $link.text($link.attr('data-add-subscription-label'));
                $link.attr('href', $link.attr('data-add-subscription-href'));
            }

            // Swap the classes
            $link.toggleClass('add-subscription delete-subscription');
        }).fail(function() { alert('I\'m sorry, we couldn\'t subscribe you. Please try again.'); });
    });
});
