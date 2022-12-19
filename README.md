<h1 align="center">
   <a href="#"> LSTM - News Headline Generator </a>
</h1>

<h3 align="center">
    💻📰 Your Computer creating News Headline! 📰💻
</h3>

<h4 align="center"> 
	 Status: Finished
</h4>
<p align="center">
 <a href="#about">About</a> •
 <a href="#how-it-works">How it works</a> • 
 <a href="#results">Results</a> • 
 <a href="#author">Author</a> • 

</p>


## About

📰 News Headline Generator - LSTM

This project consists on building an LSTM model that generates a Headline based on an initial word.

In addition to the generator, this project also includes data scrapping for the model training and an exploratory analysis.

The whole project was written in python (BeautifulSoup | Pandas | Tensorflow).

---

## How it works

This project is divided into three parts:
1. Data Gathering (Web Scrapping)
2. Exploratory Analysis
3. Model Training

### 1. Data Gathering

Before we train our model, we need to have data to use as input, but there is no structured database with news headlines available.

So, the solution was to built a scrapper to get the headlines from the largest news portals in Brazil.

The headlines were scrapped from the following portals:
* [Band](https://www.band.uol.com.br)
* [BBC](https://www.bbc.com/portuguese)
* [Brasil de Fato](https://www.brasildefato.com.br/)
* [Carta Capital](https://www.cartacapital.com.br/)
* [Conexão Política](https://www.conexaopolitica.com.br/)
* [Deutsche Welle](https://www.dw.com/pt-br/not%C3%ADcias/s-7111)
* [El Pais](https://brasil.elpais.com/)
* [Estadão](https://www.estadao.com.br/)
* [Folha de SP](https://www.folha.uol.com.br/)
* [Gazeta do Povo](https://www.gazetadopovo.com.br/)
* [Globo](https://www.globo.com/)
* [iG](https://www.ig.com.br/)
* [Isto É](https://istoe.com.br/)
* [Jornal da Cidade](https://www.jornaldacidadeonline.com.br/)
* [Pleno News](https://pleno.news/)
* [R7](https://www.r7.com/)
* [Renova Mídia](https://renovamidia.com.br/)
* [Revista Forúm](https://revistaforum.com.br/)
* [Terça Livre](https://tercalivre.com.br/)
* [UOL](https://www.uol.com.br/)
* [Veja](https://veja.abril.com.br/)


**Techniques**:

To get the headlines, all websites from all portals were analyzed to understand their structureand how to scrap them.

BeautifulSoup and Requests were used in the process of retrieving data from all websites.

--

**Results**:

The headlines were scrapped from 25.07 to 14.10.21, resulting on a total of 96.861 headlines (they are found in the [Manchetes](https://github.com/hlweber/Headline-News-Generator/tree/main/Manchetes) directory) with the following distribution per Portal:

![](assets/Total-Headlines-Portal.png)

--

### 2. Exploratory Analysis



--

### 3. Model Training

NEAT is a model that mutates and evolves given a fitness value - in this case, the greatest the fitness, the better.

In this model, the fitness increases when the car hits a checkpoint or finishes a lap.

And the fitness reduces when the car moves backwards or hits a wall.

For every car in each frame the model receives six inputs:

1. Car Angle
2. Distance to the wall if the angle was decreased by -90°
3. Distance to the wall if the angle was decreased by -45°
4. Distance to the wall if the angle was kept the same
5. Distance to the wall if the angle was increased by 45°
6. Distance to the wall if the angle was increased by 90°

And the model gives two outputs either the car should move forward, backward or do nothing. And either the car should rotate to the left, to the right or do nothing.

---

## Results

The computer was able to complete an lap after a few generations, put there are some room for improvement.

First, the best generation moves almost like an ant, changing its direction a lot, even when is not necessary, maybe implementing a mechanic that reduces the car speed when making a turn, would solve this behaviour.

Second, the increase of the fitness currently does not have relationship with time elapsed, adjusting this could make the cars goes faster

Lastly, the track is not perfect, there are some wall points that are not visual in some parts of the track that makes the car collide when it shouldn’t have.

Despite that, it's easy to perceive the evolution of the generations and the success of this model.


![](assets/evolution-racing_game.gif)

---

## Author

#### Henrique L. Weber

[![Linkedin Badge](https://img.shields.io/badge/-LinkedIn-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/henrique-weber/)](https://www.linkedin.com/in/henrique-weber/) 
[![Gmail Badge](https://img.shields.io/badge/-Email-c14438?style=flat-square&logo=Gmail&logoColor=white&link=mailto:hlweber@uol.com.br)](mailto:hlweber@uol.com.br)
