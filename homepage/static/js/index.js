$(function () {
  $("#inputType").change(function () {
    
    var SelectedValue = $(this).val();

    switch (SelectedValue) {
      case "name":
        console.log("name");
        $("#inputContent").attr("pattern", ".*");
        break;
      case "nat_id":
        console.log("nat");
        $("#inputContent").attr("pattern", "\\d{13}");
        $("#inputContent").inputmask();
        break;
      default:
        console.log("default");
        $("#inputContent").attr("pattern", "^\\d{10}$|^\\d{12}$|^\\d{14}$");
        $("#inputContent").inputmask();
    }
  });

  $("#SearchForm").submit(function (event) {
    // Stop form from submitting normally
    $("#loadresponse").css({ display: "inline" });
    $("#ResponseTrue").css({ display: "none" });
    $("#ResponseFalse").css({ display: "none" });

    event.preventDefault();

    var requrl =
      "/api/query?type=" +
      $("#inputType").val() +
      "&content=" +
      $("#inputContent").val();

    var req = $.get(requrl)
      .done(function (data) {
        $("#loadresponse").css({ display: "none" });

        if (data.value == true) {
          $("#ResponseTrue").css({ display: "contents" });
          $("#ResponseFalse").css({ display: "none" });
          $("#ResponseTrue").text(
            "พบในฐานข้อมูล ผู้ขายมีประวัติการโกงทั้งหมด " +
              data.count +
              " รายการ"
          );
        } else {
          $("#ResponseTrue").css({ display: "none" });
          $("#ResponseFalse").css({ display: "contents" });
        }
      })
      .fail(function (data) {
        console.err("Response error: " + data);
        // 4xx or 5xx response, alert user about failure
      });
  });
  
});
