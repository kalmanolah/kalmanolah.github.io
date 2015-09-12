Title: Improving Jenkins Pipeline Speeds By Lowering Quiet Periods
Date: 2014-06-12T18:30:11+02:00
Tags: Performance, Continuous delivery/integration/deployment, Jenkins CI, Horrible

_Disclaimer: If you've ever looked at the "quiet period" feature before, this
blog post will be extremely boring to you._

So today was the first time I took a real look at the [quiet period][1] setting
available to Jenkins jobs.

I had created a pipeline using the [build flow plugin][2] consisting of two
jobs (three if you include the actual pipeline). According to the
[build graph view][3], all of the individual jobs took only 2.4 seconds to run,
combined. Yet, the pipeline took a whopping **10 whole seconds** to run. Here's
a screenshot:

![pipeline view - before][4]

After a bit of snooping around I stumbled upon the single most useless feature
to ever get included in any application (imvho): "quiet period". You can find
that on your job configuration page, under "Advanced Project Options".

The quiet period feature basically prevents a job from running for _x_ seconds
after it's been scheduled. This would be useful in a variety of situations,
according to some credible sources. The default value is set to **5**. **5 whole
seconds**. **Per job.** That you're _**never**_ getting back.

Here's my pipeline after I'd set the quiet period to 0 seconds:

![pipeline view - after][5]

You're welcome. Feel free to tell me why I did a bad thing.

[1]: http://jenkins-ci.org/content/quiet-period-feature
[2]: https://wiki.jenkins-ci.org/display/JENKINS/Build+Flow+Plugin
[3]: https://wiki.jenkins-ci.org/display/JENKINS/Build+Graph+View+Plugin
[4]: {filename}/assets/img/jenkins_pipeline_1.png
[5]: {filename}/assets/img/jenkins_pipeline_2.png
