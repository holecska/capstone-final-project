
let auth0 = null;

const fetchAuthConfig = () => fetch("/auth_config.json");

// ..

const configureClient = async () => {
  const response = await fetchAuthConfig();
  const config = await response.json();

  auth0 = await createAuth0Client({
    domain: config.domain,
    client_id: config.clientId
  });
};

//https://holecska.eu.auth0.com/authorize?audience=capstone_identifier&response_type=token&client_id=qhDJV70svVcNnjRkHUUtxqODyFqz1lTJ&redirect_uri=https://localhost:8080/login
// ..

window.onload = async () => {
  await configureClient();

  //NEW - update the UI state
  updateUI();

  const isAuthenticated = await auth0.isAuthenticated();

  if (isAuthenticated) {
    // show the gated content
    return;
  }

  // NEW - check for the code and state parameters
  const query = window.location.search;
  if (query.includes("code=") && query.includes("state=")) {

    // Process the login state
    await auth0.handleRedirectCallback();


    updateUI();

    // Use replaceState to redirect the user away and remove the querystring parameters
    window.history.replaceState({}, document.title, "/");
  }
};

// NEW
  const updateUI = async () => {
  const isAuthenticated = await auth0.isAuthenticated();

  document.getElementById("btn-logout").disabled = !isAuthenticated;
  document.getElementById("btn-login").disabled = isAuthenticated;
};

// ..

const login = async () => {
  await configureClient();
  await auth0.loginWithRedirect({
    redirect_uri: "https://localhost:8080/login"
  })
  .then(function(res){
    console.log(res)
  })
};

const logout = async () => {
  auth0.logout({
  client_id: null,
  returnTo: 'http://localhost:8080/logout'
});
}

// jwt = response.jwt
// localStorage.setItem("token",jwt)
