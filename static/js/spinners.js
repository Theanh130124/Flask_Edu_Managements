//document.addEventListener("DOMContentLoaded", function () {
//        var spinnerOverlay = document.getElementById("spinner-overlay");
//
//        // Hiển thị spinner khi trang tải
//        spinnerOverlay.style.display = "flex";
//
//        // Ẩn spinner sau 2 giây (hoặc bạn có thể điều chỉnh thời gian)
//        setTimeout(function () {
//            spinnerOverlay.style.display = "none";
//        }, 2000);  // Thời gian (2 giây)
//
//        // Thêm sự kiện cho các liên kết và form
//        document.querySelectorAll("a, form").forEach(element => {
//            element.addEventListener("click", function () {
//                spinnerOverlay.style.display = "flex";
//            });
//        });
//    });