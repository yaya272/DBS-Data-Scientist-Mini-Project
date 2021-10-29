from typing import List, Union

import pandas as pd
from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel, validator
from app import database as db
import joblib

from utils import remove_stops, replace

#########################
# Load Model & Pipeline #
#########################
label_encoder = joblib.load("../models/label_encoder.bin")
preprocessing_pipeline = joblib.load("../models/preprocessing_pipeline.bin")
model = joblib.load("../models/final_model.bin")

####################
# Define Namespace #
####################
g_router = APIRouter(
    prefix="/genre",
    tags=["Music Genre"]
)


##################
# Req/Res Models #
##################
class MusicRecord(BaseModel):
    trackID: Union[int, None]
    title: Union[str, None]
    tags: Union[str, None]
    loudness: Union[float, None]
    tempo: Union[float, None]
    time_signature: Union[int, None]
    key: Union[int, None]
    mode: Union[int, None]
    duration: Union[float, None]
    vectors: List[Union[float, None]]

    # Check if the vectors list has 148 items (can be null)
    @validator("vectors")
    def check_vector_size(cls, v):
        assert len(v) == 148, "Vect feature must contain 148 data points"
        return v


class GenrePredictRequest(BaseModel):
    data: List[MusicRecord]


class GenrePredictResponse(BaseModel):
    title: str
    genre: str


#############
# Endpoints #
#############
@g_router.post("/predict",
               status_code=status.HTTP_200_OK,
               response_model=List[GenrePredictResponse],
               summary="Make prediction")
def predict(request_data: GenrePredictRequest):
    records = []
    for record in request_data.data:
        records.append(record.dict())

    # Reshape vectors from 1 list to 148 features
    records = pd.DataFrame(records)
    vectors = records["vectors"]
    records.drop(columns=["vectors"], inplace=True)
    vectors = pd.DataFrame(vectors.tolist())
    names = {i: f"vect_{i + 1}" for i in range(148)}
    vectors.rename(names, axis=1, inplace=True)
    records = pd.concat([records, vectors], axis=1)

    # Preprocessing & Prediction
    records["tags"] = records["tags"].str.replace(",", "")
    X = preprocessing_pipeline.transform(records)
    genres = model.predict(X).argmax(axis=1)
    genres = label_encoder.inverse_transform(genres)
    titles = records["title"].values

    genre_dict = db.get_genre_by_names(genres)
    response = []
    data_to_insert = []
    for title, genre in zip(titles, genres):
        response.append(GenrePredictResponse(genre=genre, title=title))
        data_to_insert.append((title, genre_dict[genre]))
    db.insert_title(data_to_insert)
    return response


@g_router.get("/",
              status_code=status.HTTP_200_OK,
              response_model=List[str],
              summary="Retrieve the list of existing genre.")
def get_genre():
    genres = db.get_genre()
    genres = [genre[0] for genre in genres]
    if not genres:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Genre found in the database")
    return genres


@g_router.get("/{genre}/",
              status_code=status.HTTP_200_OK,
              response_model=List[str],
              summary="Get all music title from a specific genre")
def get_title(genre: str):
    titles = db.get_title_by_genre(genre)
    titles = [title[0] for title in titles]
    if not titles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Genre: {genre} doest not exist")

    return titles
