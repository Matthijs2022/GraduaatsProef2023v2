import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { getBedrijven } from '../util/api.js';
import React, { useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios';
import { Link } from 'react-router-dom';

const Body = () => {
  const navigate = useNavigate();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const [bedrijven, setBedrijven] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    getBedrijven().then((bedrijven) => {
      setBedrijven(bedrijven);
      setIsLoading(false);
    });
  }, []);

  const onSubmit = async (data) => {
    try {
      // Check if the user already exists
      const checkUserResponse = await axios.get(
        `https://localhost:7020/api/Bezoeker/GetBezoek/${data.email}` //http://127.0.0.1:5000/bezoeker/email/test@test.com werkt al!!
      );
      if (checkUserResponse.data) {
        // als hij al bestaat voegen we de bestaande bezoekeer toe aan de bezoek tabel
        console.log('User already exists:', checkUserResponse.data);

        const bezoekerId = checkUserResponse.data.id;

        const bezoek = {
          id: 0,
          bedrijfId: data.bedrijfId,
          bezoekerId: bezoekerId,
          bezochtteWerknemer: data.bezochtewerknemer,
          startTijd: new Date().toISOString(),
          eindTijd: null,
          status: 1,
        };

        const bezoekResponse = await axios.post(
          'https://localhost:7020/api/Bezoek',
          JSON.stringify(bezoek),
          {
            headers: {
              'Content-Type': 'application/json',
            },
          }
        );
        console.log('Bezoek successfully created:', bezoekResponse.data);

        navigate('/vertrek');
      } else {
        // Bestaat hij niet, dan maken we een nieuwe bezoeker aan
        const response = await axios.post(
          'https://localhost:7020/api/Bezoeker',
          JSON.stringify(data),
          {
            headers: {
              'Content-Type': 'application/json',
            },
          }
        );
        console.log('Bezoeker successfully created:', response.data);
        const bezoekerId = response.data.id;

        const bezoek = {
          id: 0,
          bedrijfId: data.bedrijfId,
          bezoekerId: bezoekerId,
          bezochtteWerknemer: data.bezochtewerknemer,
          startTijd: new Date().toISOString(),
          eindTijd: null,
          status: 1,
        };

        const bezoekResponse = await axios.post(
          'https://localhost:7020/api/Bezoek',
          JSON.stringify(bezoek),
          {
            headers: {
              'Content-Type': 'application/json',
            },
          }
        );
        console.log('Bezoek successfully created:', bezoekResponse.data);

        navigate('/vertrek');
      }
    } catch (error) {
      console.error('Error creating Bezoeker:', error);
      console.log('Response data:', error.response.data);
      const { errors } = error.response.data;
      console.log('Validation errors:', errors);
    }
  };

  return (
    <>
      <div className="flex h-screen justify-center items-end start-scherm-wrapper"></div>
      <div className="heading text-center mt-4">
        <h1 className="display-3">Welkom!</h1>
      </div>
      <form
        className="form-horizontal text-center border-4 container"
        onSubmit={handleSubmit(onSubmit)}
      >
        {/* Form fields */}
        <div className="control-group">
          <label className="control-label text-lg" htmlFor="Voornaam">
            Voornaam
          </label>
          <div className="controls">
            <input
              type="text"
              id="Voornaam"
              {...register('voornaam', { required: true })}
              placeholder=""
            />
            {errors.voornaam && (
              <div>
                <span>
                  <font color="red">This field is required</font>
                </span>
              </div>
            )}
          </div>
        </div>
        <div className="control-group">
          <label className="control-label" htmlFor="Achternaam">
            Achternaam
          </label>
          <div className="controls">
            <input
              type="text"
              id="Achternaam"
              {...register('achternaam', { required: true })}
              placeholder=""
            />
            {errors.achternaam && (
              <div>
                <span>
                  <font color="red">This field is required</font>
                </span>
              </div>
            )}
          </div>
        </div>
        <div className="control-group">
          <label className="control-label" htmlFor="Email">
            Email
          </label>
          <div className="controls">
            <input
              type="text"
              id="Email"
              {...register('email', {
                required: true,
                pattern: {
                  value:
                    /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/,
                  message: 'Invalid email address',
                },
              })}
              placeholder="Enter your email"
            />
            {errors.email && (
              <div>
                <span>
                  <font color="red">Geef een correct email in</font>
                </span>
              </div>
            )}
          </div>
        </div>
        <div className="control-group">
          <label className="control-label mx-3" htmlFor="Bedrijf">
            Bedrijf
          </label>
          <select
            {...register('bedrijfId', { required: true })}
            className="border-2 border-gray-600 rounded-lg text-xl hover:border-black mt-3 mb-1 p-2 hover:p-3 hover:mt-2 hover:mb-0"
          >
            {bedrijven.map((obj) => (
              <option key={obj.id} value={obj.id}>
                {obj.naam}
              </option>
            ))}
          </select>
          {errors.bedrijfId && (
            <div>
              <span>
                <font color="red">This field is required</font>
              </span>
            </div>
          )}
        </div>
        <div className="control-group">
          <label className="control-label" htmlFor="Bezocht">
            Wie bezoekt u?
          </label>
          <div className="controls">
            <input
              type="text"
              id="Bezocht"
              {...register('bezochtewerknemer', { required: true })}
              placeholder=""
            />
            {errors.bezochtewerknemer && (
              <div>
                <span>
                  <font color="red">This field is required</font>
                </span>
              </div>
            )}
          </div>
        </div>
        <div className="control-group" />
        <div className="controls">
          <button type="submit" className="btn btn-primary btn-lg mt-4">
            Verder
          </button>
        </div>
      </form>
      <div className="controls text-center">
        <Link to="/" className="btn btn-primary btn-lg mt-4">
          Terug
        </Link>
      </div>
    </>
  );
};

export default Body;
