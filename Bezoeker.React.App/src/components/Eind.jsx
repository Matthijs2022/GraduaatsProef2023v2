import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';

const Eind = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();
  const navigate = useNavigate();
  const [isSubmitted, setIsSubmitted] = useState(false);

  useEffect(() => {
    if (isSubmitted) {
      const timer = setTimeout(() => {
        navigate('/');
      }, 5000);

      return () => clearTimeout(timer);
    }
  }, [isSubmitted, navigate]);

  const onSubmit = async (data) => {
    try {
      const endResponse = await axios.post(`http://127.0.0.1:5000/bezoek/end`, {
        email: data.email,
      });
      console.log(data.email);

      if (endResponse.data) {
        console.log('Bezoek successfully deleted:', endResponse.data);
        setIsSubmitted(true);
      }
    } catch (error) {
      console.error('Error retrieving Bezoeker:', error);
      console.log('Response data:', error.response.data);
      const { errors } = error.response.data;
      console.log('Validation errors:', errors);
    }
  };

  return (
    <>
      {isSubmitted ? (
        <>
          <div className="p-5 text-center"></div>
          <div className="p-5 text-center">
            <div className=" heading text-center mt-24">
              <h1 className="display-1 mt-20">Bedankt voor uw bezoek</h1>
            </div>
          </div>
        </>
      ) : (
        <>
          <div className="p-5 text-center"></div>
          <div className="p-5 text-center">
            <div className=" heading text-center mt-24">
              <h1 className="display-1 mt-20">Uitschrijven bij vertrek</h1>
            </div>
          </div>
          <form
            className="control-group text-center"
            onSubmit={handleSubmit(onSubmit)}
          >
            <label className="control-label" htmlFor="email">
              Wat is uw ingevoerde email?
            </label>
            <div className="controls">
              <input
                type="text"
                id="Email"
                {...register('email', {
                  required: true,
                  pattern: {
                    value:
                      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/,
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

            <div className="controls text-center">
              <button type="submit" className="btn btn-primary btn-lg mt-4">
                Verder
              </button>
            </div>
          </form>
        </>
      )}

      <div className="controls text-center py-3">
        <Link to="/" className="btn btn-primary btn-lg px-4 py-2">
          Terug
        </Link>
      </div>
    </>
  );
};

export default Eind;
