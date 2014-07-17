jQuery(document).ready(function($) {
    $(".vote_form").submit(function(e) {
        e.preventDefault();
        var btn = $("button", this);
        var l_id = $(".hidden_id", this).val();
        btn.attr('disabled', true);
        $.post("/vote/", $(this).serializeArray(),
        function(data) {
            var int = parseInt($("#vote_count").text());
            if (data["voteobj"]) {
                btn.addClass("deeppink");
                // #todo change current # of votes
            } else {
                btn.removeClass("deeppink")
            }
        });
        btn.attr('disabled', false);
    });
});