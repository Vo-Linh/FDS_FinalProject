
from inference import *
import gradio as gr
import random

from fastapi import FastAPI

app = FastAPI()
@app.get("/")
def read_main():
    return {"message": "This is your main app"}

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            street = gr.Dropdown(
                label="Street",
                choices = street,
            )

            statezip = gr.Dropdown(
                label="State Zip",
                choices=statezip,    
            )
            city = gr.Dropdown(
                label="City",
                choices=city, 
            )

            sqft_living = gr.Slider(
                label="Sqrt living",
                minimum=0,
                maximum=10000,
                step=50,
                randomize=True,
            )

            sqft_above = gr.Slider(
                label="Sqrt above",
                minimum=0,
                maximum=10000,
                step=50,
                randomize=True,
            )

            bathrooms = gr.Slider(
                label="Bathrooms",
                minimum=0,
                maximum=5,
                step=1,
                randomize=True,
            )

            sqft_lot = gr.Slider(
                label="Sqft lot",
                minimum=0,
                maximum=20000,
                step=50,
                randomize=True,
            )

            floors = gr.Slider(
                label="Floors",
                minimum=0,
                maximum=7,
                step=0.5,
                randomize=True,
            )

            yr_built = gr.Slider(
                label="Year Built",
                minimum = 1990,
                maximum = 2022,
                step = 1,
                randomize=True,
            )

            bedrooms = gr.Slider(
                label="Bedrooms",
                minimum = 0,
                maximum = 10,
                step = 1,
                randomize=True,
            )

            view = gr.Slider(
                label="View",
                minimum = 0,
                maximum = 4,
                step = 1,
                randomize=True,
            )

            sqft_basement = gr.Slider(
                label="Sqft basement",
                minimum = 0,
                maximum = 3000,
                step = 50,
                randomize=True,
            )

            yr_renovated = gr.Slider(
                label="Year Renovated",
                minimum = 1912,
                maximum = 2022,
                step = 1,
                randomize=True,
            )


        with gr.Column():
                    label = gr.Text(value = "Price")
                    with gr.Row():
                        predict_btn = gr.Button(value="Predict")

                    predict_btn.click(
                        predict,
                        inputs=[
                            street,
                            statezip,
                            city,
                            sqft_living,
                            sqft_above,
                            bathrooms,
                            sqft_lot,
                            floors,
                            yr_built,
                            bedrooms,
                            view, 
                            sqft_basement,
                            yr_renovated,
                        ],
                        outputs=label,
            )

app = gr.mount_gradio_app(app, demo, path="/gradio")
# demo.launch(share=True, debug=True)