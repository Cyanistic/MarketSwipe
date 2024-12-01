
const LoginPage = () => {
    return (
      <div style={styles.container}>
        {/* Title */}
        <div style={styles.titleContainer}>
          <h1 style={styles.text}>MARKET</h1>
          <h1 style={styles.text}>SWIPE</h1>
        </div>
  
        {/* Image Box */}
        <div style={styles.box}>
          <img
            src="/./components/StartLogo.png" 
            alt="Cart with arrows"
            style={styles.image}
          />
        </div>
  
        {/* Form */}
        <div style={styles.formSection}>
          <h3 style={styles.signInText}>SIGN IN</h3>
          <div style={styles.formContainer}>
            {/* Username Input */}
            <div style={styles.inputGroup}>
              <span style={styles.icon}>👤</span>
              <input
                type="text"
                placeholder="Username"
                style={styles.input}
              />
            </div>
  
            {/* Password Input */}
            <div style={styles.inputGroup}>
              <span style={styles.icon}>🔒</span>
              <input
                type="password"
                placeholder="Password"
                style={styles.input}
              />
            </div>
  
            {/* Buttons */}
            <button style={styles.loginButton}>LOG IN</button>
            <button style={styles.signUpButton}>SIGN UP</button>
          </div>
        </div>
      </div>
    );
  };
  
  const styles = {
    container: {
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      height: '100vh',
      backgroundColor: '#FFD8A9',
      textAlign: 'center',
    },
    titleContainer: {
      marginBottom: '20px',
    },
    text: {
      color: '#39B647',
      fontSize: '7rem',
      fontWeight: 'bold',
      fontFamily: "'Poppins', sans-serif",
      margin: 0,
    },
    box: {
      width: '373px',
      height: '256px',
      backgroundColor: '#FFF',
      borderRadius: '10px',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
      marginBottom: '30px',
    },
    image: {
      maxWidth: '130%',
      maxHeight: '130%',
      marginLeft: '125px',
      marginTop: '125px',
    },
    formSection: {
      width: '100%',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
    },
    signInText: {
      color: '#888',
      fontSize: '1.5rem',
      fontWeight: 'bold',
      fontFamily: "'Poppins', sans-serif",
      marginBottom: '20px',
    },
    formContainer: {
      width: '300px',
      display: 'flex',
      flexDirection: 'column',
      gap: '15px',
    },
    inputGroup: {
      display: 'flex',
      alignItems: 'center',
      backgroundColor: '#FFF',
      borderRadius: '10px',
      padding: '10px',
      boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
    },
    icon: {
      marginRight: '10px',
      fontSize: '1.5rem',
      color: '#888',
    },
    input: {
      border: 'none',
      outline: 'none',
      flex: 1,
      fontSize: '1rem',
      fontFamily: "'Poppins', sans-serif",
      padding: '5px',
    },
    loginButton: {
      backgroundColor: '#444',
      color: '#FFF',
      fontSize: '1rem',
      fontFamily: "'Poppins', sans-serif",
      padding: '10px',
      borderRadius: '10px',
      border: 'none',
      cursor: 'pointer',
    },
    signUpButton: {
      backgroundColor: '#39B647',
      color: '#FFF',
      fontSize: '1rem',
      fontFamily: "'Poppins', sans-serif",
      padding: '10px',
      borderRadius: '10px',
      border: 'none',
      cursor: 'pointer',
    },
  };
  
  export default LoginPage;
  