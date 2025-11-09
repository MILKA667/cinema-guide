import Header from '../../components/Header';
import Footer from '../../components/Footer';
import SideBar from '../../components/SideBar';
import Main from '../../components/Main';

const Home = () => {
  return (
    <div>
      <Header />
      <main>
        <SideBar />
        <Main />
      </main>
      <Footer />
    </div>
  );
};

export default Home