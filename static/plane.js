async function refresh() {
      try {
        const RES = await fetch("/current");
        const DATA = await RES.json();
        const LOGO = document.getElementById("airlinelogo");
        const PLANEBOX = document.getElementById("planeBox")

        PLANEBOX.value = DATA.plane;
        LOGO.src = DATA.logo_s3_url;
        
      }catch (_) {}
    }

    //runs the function right away
    refresh();

    //runs the fuction every 2 seconds
    setInterval(refresh, 2000);

