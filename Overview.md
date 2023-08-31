# Overview

After I accepted my PhD offer from UMD iSchool, I onboarded a cool [project](https://www.ssrc.org/grantees/a-field-experiment-to-mitigate-the-harm-of-online-misinformation/) by [Prof. Giovanni Luca Ciampaglia](https://glciampaglia.com/) and his awesome colleagues. I was lucky to start joining online weekly meetings from April 19th, 2023. 

This is an archive of what I did as an RA (more of my journey of muddling through). 



## Developing Survey Design & Questionnaire

My first ever task as an RA was to review the key papers - [Allcott et al. (2020)](https://www.aeaweb.org/articles?id=10.1257%2Faer.20190658) and [Levy (2021)](https://www.aeaweb.org/articles?id=10.1257/aer.20191777) (who is on the team!) - to make a draft survey design and questionnaire. My precise job was to see how we could adapt and employ the languages and wordings to our project's survey. Since then, I have contributed (well, I hope I did) to refining survey design and questions. 




## Testing with Twitter API 

Another important set of task was to figure out the technical aspects of experiment - mostly using Twitter APIs to do things we need. 

### DMs
- For instance, I checked whether automating sending DMs to experiment participants would be feasible using Twitter API. It was feasible, technically, but under assumption that all participants follow our study account (since sending DMs are allowed between mutual followers in most cases by setting). 

### Unfollowing 
The study's main treatment was making some participants **'unfollow'** specific accounts on Twitter. 
If we could unfollow target accounts on behalf of the treatment group, many problems including compliance and all that are solved!  


Using Twitter API, I was able to get ...
  - (1) my other account authroize my app to request granular permission, especially unfollowing function using OAuth 2.0 and setting scopes (using OAuth 1.0a for authorization may scare away participants since it asks access to lots of functions).
  - Then, (2) I was able to unfollow/re-follow specific accounts on the behalf of my another account that I got authorization from. You can find the codes here.

```diff
+ ADD LINKS TO CODES!
```



The problem was that Musk kept changning the policy and access to Twitter API, which resulted in high levels of uncertainties related to core design of the study. 

(Personal recommendation: If possible, avoid choosing X or Twitter as your social media platform to study. There are so many unpredicatble changes and moving parts that can derail your experiment! I mean, even the name of the platform has changed during the brief period of my RAship ...so...)

  - For instance, due to Musk's decision to remove the API for getting friends list, we were no longer able to get the list of accounts that participants follow. This was critical because to make them unfollow "certain" low-quality accounts, we needed to know which low-quality accounts the participants were following.


### Reverse Chrnological Feed 

I came up with a detouring idea: how about *collecting reverse chronological home timelines* using available Twitter API? If there are low-quality news sources in the collected home timelines, we know that which specific low-quality accounts the participants are following and ask them to unfollow these accounts in the study. Also, this could help us see changes in the home timelines after the treatment. 
- However, it turned out that collecting reverse chronological timelines is now capped (Thanks a lot, Musk!). It seemed nearly impossible to fit within the limitations of our Basic Twitter API access.

-----------

Let me briefly summarize here: So, the main goal was to figure out what accounts the participants are following and the reverse chronological timeline is only practicaly way for us. But the problem was that reverse chrnological endpoint was capped and our Basic access allowed only 10K tweets/month. 

The questions were: 
- Would upgrading to Pro access solve our problem? In other words, could we fit the Pro access limit if we upgrade to Pro (1M/month)?
- How much can we spend?
- How many tweets we are going to collect?
- How long does it take for us to get 1M cap?
- How many pulls/tweets should we collect for us to have a sense of what accounts the participants are following?
- In other words, **when do we stop pulling** the reverse chronological timelines?


Giovanni had the clever idea that we could stop pulling the tweets if we reach a point where additional pull is not worth it. 

Let's say that you have the number of tweets pulled on your x-axis. And on the y-axis, you have the number of distinct accounts appeared in your timeline. So by plotting the number of disctint accounts against the number of tweets collected from the timeline, we could determine where the plot becomes flat. In general, the plot will increase rapidly because as you collect more tweets, you see more accounts. But it will slow down at some point since you now  have already seen majority of accounts. 

I thought that was an excellent plan of action! And here comes my muddling through with the pilot data analysis! 



## Pilot Data Analysis: Finding Knees 

Luckily, we had pilot data from another project that I could use to test different plots and estimate the knees (where the plot slows down). During the summer (July and August), I worked really hard to create plots in various ways and (sort of failed but) tried to nail down a number on which we could base our decision. 

Here is the [link]() to a folder where I put all of my notebooks (html files created with R markdown) in chronological order. 

```diff
+ ADD LINKS TO CODES!
```

### END OF THE AUGUST (AFTER I ARRIVED IN COLLEGE PARK)
- Wrap up with the pilot data analysis
- Design change: Muting -> Writing codes 
- Backend (SSH) + JavaScript embedded in Qualtrics + IRB...
(Soon to be added) 


