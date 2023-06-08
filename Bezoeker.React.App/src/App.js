import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";

// Importeren van uw component
import Header from "./components/header";
import Body from "./components/BezoekerForm";
import Eind from "./components/Eind";
import {
  Route,
  RouterProvider,
  createBrowserRouter,
  createRoutesFromElements,
} from "react-router-dom";
import StartScherm from "./components/StartScherm";

const router = createBrowserRouter(
  createRoutesFromElements(
    <>
      <Route
        path="/"
        element={
          <>
            <StartScherm />
          </>
        }
        // loader={ParkingLoader}
      />
      <Route
        path="/aankomst"
        element={
          <>
            <Body />
          </>
        }
      />
      <Route
        path="/vertrek"
        element={
          <>
            <Eind />
          </>
        }
      />
    </>
  )
);

function App() {
  return <RouterProvider router={router} />;
}
export default App;
