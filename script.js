document.addEventListener("DOMContentLoaded", function () {
  fetch("https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment.json")
    .then(response => response.json())
    .then(data => {
      const results = data.result.results;
      const promotionElements = document.querySelectorAll(".promotion");
      const titleElements = document.querySelectorAll(".title_text")
      for (let i = 0; i < promotionElements.length; i++) {
        let newTextNode = document.createTextNode(results[i].stitle);
        promotionElements[i].appendChild(newTextNode);
      }
      for (let i = 0; i < titleElements.length; i++) {
        let newTextNode = document.createTextNode(results[i + promotionElements.length].stitle);
        titleElements[i].appendChild(newTextNode);
      }
      const top_imgs = document.querySelectorAll(".landscape_head")
      const body_imgs = document.querySelectorAll(".landscape")
      for (let i = 0; i < top_imgs.length; i++) {
        const file = results[i].file;
        const start_idx = file.indexOf("http://");
        const end_idx = file.toLowerCase().indexOf(".jpg", start_idx) + 4;//從start_idx尋找下一個http://
        const firstURL = file.substring(start_idx, end_idx !== -1 ? end_idx : undefined)
        const imgElement = document.createElement("img");//創立img物件
        imgElement.src = firstURL;
        imgElement.classList.add("landscape_head");
        const top_img = top_imgs[i];
        top_imgs[i].parentNode.replaceChild(imgElement, top_img);
      }
      for (let i = 0; i < body_imgs.length; i++) {
        const file = results[i + 3].file;
        const start_idx = file.indexOf("http://");
        const end_idx = file.toLowerCase().indexOf(".jpg", start_idx) + 4;
        const firstURL = file.substring(start_idx, end_idx !== -1 ? end_idx : undefined)
        const imgElement = document.createElement("img");
        imgElement.src = firstURL;
        imgElement.classList.add("landscape");
        body_imgs[i].parentNode.replaceChild(imgElement, body_imgs[i]);
      }
    });
})
