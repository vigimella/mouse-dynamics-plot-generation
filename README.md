
# MDPG (Mouse Dynamics Plot Generator)

MDPG is a script written in Python language able to convert the user's 
sessions stored in [Balabit Mouse-Dynamics-Challenge](https://github.com/balabit/Mouse-Dynamics-Challenge) into images. As a consequence of 
a less number of sessions, we also used the augmentation technique.


## Installation

Install requirements.txt

```bash
  pip install -r requirements.txt
```

## Environment Variables

To run this project, you will need to download the [main repository](https://github.com/balabit/Mouse-Dynamics-Challenge), and add the following environment variables to your .env file

`TRAINING_FOLDER_URL = 'path/to/training_files'`

`TEST_FOLDER_URL = 'path/to/test_files'`


## Authors

- [@Vigimella](https://www.github.com/vigimella)
- [@FrancescoMercaldo](https://github.com/FrancescoMercaldo)


## Acknowledgements

The authors would like to thank the 'Trust, Security and Privacy' research group within the [Institute of Informatics and Telematics](https://www.iit.cnr.it/) (CNR - Pisa, Italy), that support their researches.

A special thanks to Fülöp, Á., Kovács, L., Kurics, T., Windhager-Pokol, E. (2016). Balabit Mouse Dynamics Challenge data set. Available at: https://github.com/balabit/Mouse-Dynamics-Challenge
