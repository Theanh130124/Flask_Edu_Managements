//document.addEventListener("DOMContentLoaded", function () {
//        var spinnerOverlay = document.getElementById("spinner-overlay");
//
//        // Hiển thị spinner khi trang tải
//        spinnerOverlay.style.display = "flex";
//
////      Fix thời gian spinners
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