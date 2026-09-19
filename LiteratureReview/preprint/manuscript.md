---
title: "Computational analysis of the COVID-19 modelling literature"
subtitle: "A selective narrative review of studies published in 2020–2024"
fontsize: 11pt
geometry: margin=1in
colorlinks: true
---

## Abstract

Mathematical models of COVID-19 addressed several distinct questions: how transmission changed, how many infections escaped detection, what interventions might achieve, and how vaccination altered epidemic outcomes. These questions require different assumptions and forms of evidence. This selective narrative review examines 28 studies published between 2020 and 2024, drawing primarily on an existing collection of papers. It compares compartmental representations, stochastic and statistical inference, intervention scenarios, vaccination and variant models, and forecast evaluation through three recurring issues: the relationship between infections and observations, the treatment of changing transmission, and the interpretation of uncertainty. The synthesis distinguishes fitted epidemic trajectories from forecasts and counterfactual scenarios. Across the selected examples, the usefulness of a model depends on how closely its structure, data, and evaluation match its intended question. Additional biological detail can improve the representation of a mechanism while introducing parameters that the available observations cannot independently identify. The review offers a compact framework for reading COVID-19 modelling studies critically; it does not provide an exhaustive survey, a pooled estimate of intervention effects, or an assessment of current policy.

**Keywords:** COVID-19; transmission models; compartmental models; parameter inference; uncertainty; narrative review.

## 1. Introduction

COVID-19 modelling brought the relationship between mathematical assumptions and public decisions into unusually sharp focus. A curve fitted to reported cases, an estimate of time-varying transmission, and a simulation of an alternative vaccination programme may all produce an epidemic trajectory. They nevertheless answer different questions. Their conclusions should be interpreted in relation to the quantities being estimated, the data used for calibration, and the assumptions governing unobserved processes.

Bertozzi et al. [1] illustrated the value of relatively parsimonious models by relating exponential growth, branching processes, and susceptible–infectious–removed (SIR) dynamics to different stages of an epidemic. Their comparison provides a useful starting point: model complexity is a choice about which mechanisms to resolve. It is not, by itself, evidence of predictive quality.

This review asks: **how do model structure and data limitations affect the interpretation of COVID-19 transmission studies?** It concentrates on population-level transmission and its estimation, with examples concerning non-pharmaceutical interventions, vaccination, variant competition, statistical surveillance, and forecast evaluation. The aim is a critical synthesis of methodological lessons from the early pandemic literature, rather than a catalogue of every modelling approach.

## 2. Literature collection and computational processing

### 2.1. Retrieval and metadata preparation

The starting literature collection was assembled using the Semantic Scholar API in approximately August 2024, according to the author's recollection; the exact retrieval date was not recorded in the retained files. The saved retrieval scripts combine COVID-19 and SARS-CoV-2 terms with modelling-related expressions, including the British and American spellings of modelling, Bayesian inference, mathematical modelling, and case infection. A later script also includes metapopulation-related terms. The queries apply a Mathematics field-of-study filter and retrieve successive result batches using the API's pagination token. This filter defines a disciplinary starting point rather than comprehensive coverage of epidemiological research.

Results were saved as JSON Lines files, retaining paper identifiers and available metadata such as titles, abstracts, authors, publication dates, journal information, and open-access PDF links. The later saved dataset also contains citation information and BibTeX records. The two retained retrieval files contain 9,997 and 10,042 records respectively, with distinct paper identifiers within each file. They are alternative saved collections and must not be added together as independent search yields. These counts describe the local files, not the number of relevant or included studies.

Conversion scripts flatten nested metadata into tabular CSV files, including author information, publication venues, PDF links, and citation fields. Separate routines clean PDF URL strings and extract bibliographic information. The files document successive versions of this process; they do not establish that every record passed through a single, unchanged pipeline. In particular, the current retrieval script and the saved metadata fields are not identical, so the script should be treated as evidence of the retrieval approach rather than a complete record of the original API request.

### 2.2. Text extraction and preliminary classification

The processing scripts attempt to obtain PDF text where a link is available, using Python PDF extraction libraries. Retrieval and extraction failures receive explicit labels, including missing URLs and unreadable PDFs. A separate classifier searches titles and abstracts, allowing preliminary organisation when full text is unavailable.

Classification uses case-insensitive keyword rules for logistic regression, random forests, support vector machines, SIR-type models, ARIMA, stochastic models, and agent-based models. The implementation returns the first matching category. A reconciliation routine compares the full-text and title/abstract labels: matching labels are retained, an available label can be used when the other source is missing or uninformative, and conflicting classifications are marked for reading. These flags indicate a need for inspection; they do not demonstrate that manual inspection was completed.

The labels are organisational aids rather than validated descriptions of each paper's principal method. A keyword may occur in background material or references, while a paper can use several approaches. The first-match rule also makes classification depend on the order of the categories. Consequently, these labels are not used here to estimate the prevalence or comparative quality of model families.

### 2.3. Automated summaries and reading priorities

The final summarisation workflow used Ollama. The retained implementation is configured with Llama 2 13B and supplies each paper's abstract together with its BibTeX entry, requesting a summary of no more than 200 words that includes the author names. Thus, this workflow produces abstract-based summaries rather than full-text analyses. Providing bibliographic information alongside the abstract supports association of each summary with its source, although generated text still requires checking against the original publication.

BART, Pegasus, and T5, including an extractive summarisation stage followed by T5 generation, were explored during preliminary experimentation and were not used as the final summarisation approach. Their scripts and intermediate outputs remain in the project directory as records of that development process. The final choice of Ollama is reported here as a workflow decision, not as evidence of superior summarisation accuracy; no comparative performance evaluation is presented in this review.

A separate prioritisation script combines the 20 most-cited records from a general collection with five from a time-dependent modelling subset. This was a reading-priority experiment, not an inclusion criterion for the present manuscript or a measure of scientific quality. The Ollama-generated summaries supported exploration and synthesis of the collection, but were not treated as independent evidence for the scientific claims retained in this review.

### 2.4. Selection for the present synthesis and reproducibility limits

The present manuscript is a selective narrative review of 28 studies published between 2020 and 2024. The selection draws on the thesis literature review and the existing local collection, supplemented by source and bibliographic checks using original articles, author manuscripts, and publisher records. Papers were chosen to cover transmission structure, under-ascertainment, parameter inference, interventions, vaccination, variant dynamics, statistical surveillance, and forecast evaluation. This purposive selection is distinct from the larger computational collection and its preliminary categories. The thesis excerpt supplies candidate references and thematic context; its automated summaries are checked rather than adopted as evidence on their own.

Where a thesis entry refers to a preprint and a corresponding journal version was identified, the journal reference is used where checked. The versions consulted for Wang et al.'s reinfection analysis and Fox et al.'s ensemble study are explicitly identified as preprints. The 2024 endpoint accommodates the January 2024 Fox preprint already cited in the thesis; it does not imply an updated systematic search through that year.

The synthesis considers each study's question, model structure, data, contribution, and interpretive limits. No effect sizes are pooled. Within-host models, clinical prediction, medical-image classification, and distributional analyses without a direct population-level surveillance or forecasting question are outside the chosen scope. The publication interval describes the selected examples rather than exhaustive coverage; developments after the approximate August 2024 collection date are not reviewed.

## 3. Model structure and the observation of infection

### 3.1. Compartmental models as explicit assumptions

Compartmental models describe transitions between epidemiological states. In a simple SIR representation, susceptible individuals become infectious and subsequently leave the infectious state. An exposed compartment introduces a latent stage; further compartments can represent detection, hospitalisation, vaccination, or loss of immunity. Each extension should correspond to a mechanism relevant to the study question and to quantities that can be constrained by data or external evidence.

Ivorra et al. [2] developed a $\theta$-SEIHRD model for China that explicitly distinguishes detected and undetected infection and represents differing clinical states. The detection fraction connects reported cases to a larger, partly unobserved infection process. Their analysis also examined the effects of calibrating with data truncated at different stages of the epidemic. This is a useful reminder that the information available after an epidemic peak differs from the information available while the outbreak is growing.

The methodological implication is broader than the particular compartments used. Adding an undetected state makes an assumption visible, but it does not automatically identify the size of that state. If several combinations of transmission and detection parameters can reproduce the observations, a close fit alone cannot determine which combination is correct. External information and sensitivity analysis are therefore relevant to interpretation, alongside goodness of fit.

Cooper et al. [3] modified an SIR framework to allow the effective susceptible population to increase during surge periods, applying it to several national and regional epidemics. This differs from the usual closed-population interpretation in which susceptible depletion is monotonic in the absence of births or immunity loss. The additional flexibility can describe changing participation in an outbreak, but the susceptible variable must be interpreted according to the model's construction rather than assumed to equal a directly enumerated population.

Network structure offers another way to alter the representation of exposure. Croccolo and Roman [4] compared a percolation-type model on random graphs with an SIR formulation using US COVID-19 data. Both approaches could fit the observed trajectory while representing contacts differently. This comparison illustrates why agreement with aggregate counts does not uniquely determine the underlying contact mechanism. Network detail is useful when the question concerns connectivity or local transmission pathways, but requires evidence beyond the aggregate epidemic curve to establish that those details are realistic.

### 3.2. Reported cases are observations of a hidden process

Kucharski et al. [5] combined a stochastic transmission model with multiple datasets concerning Wuhan and internationally exported cases. Their study estimated changes in transmission and examined the probability that introductions would establish outbreaks elsewhere. Combining information from different observation settings helped address a question that a single case series could not fully resolve.

For interpretation, it is useful to distinguish infection events from their eventual observation. Reported cases depend on detection and reporting, as well as on underlying incidence. Admissions and deaths introduce further relationships involving disease progression and delays. A change in a reported series can therefore reflect a change in transmission, a change in observation, or both.

This distinction also clarifies what a fitted model has demonstrated. Reproducing reported cases shows compatibility with those observations under a specified observation model. It does not independently validate every inferred latent compartment. Comparisons against additional data are particularly informative when those data constrain different parts of the model.

Anastassopoulou et al. [6] fitted a susceptible–infectious–recovered–dead model to early Hubei data and repeated their analysis under alternative assumptions about the scale of unreported infections and recoveries. The resulting differences in estimated epidemic quantities illustrate sensitivity to ascertainment assumptions. Such alternatives are scenario analyses; multiplying reported counts does not independently measure the missing infections.

Watson et al. [7] addressed under-ascertainment in Damascus using mortality information beyond the official COVID-19 series. Their transmission analysis used all-cause mortality and checked the inferred epidemic against community-uploaded obituary notifications. This regional example shows how additional observation streams can be informative where routine surveillance is incomplete. It also makes the data source part of the substantive interpretation: estimates depend on what those mortality indicators capture and on the assumptions connecting mortality to infection.

## 4. Changing transmission and uncertainty

### 4.1. Time variation requires interpretation

Hong and Li [8] developed a time-varying SIR-based Poisson model to estimate transmission and removal rates from epidemic count data. Their work illustrates how a mechanistic model can be combined with a statistical observation framework. Allowing parameters to vary over time can describe patterns that constant-rate models cannot accommodate.

However, an estimated transmission parameter is not necessarily a measurement of a single biological property. Depending on the model, it may absorb changes in contact patterns, susceptibility, interventions, and observation. Flexibility can improve description while making causal interpretation more difficult. A useful review should therefore ask both whether a changing parameter captures the data and what processes the parameter is intended to represent.

### 4.2. Stochastic dynamics and Bayesian inference are different choices

Stochastic modelling and Bayesian inference should not be treated as interchangeable model families. Stochastic dynamics represent random variation in transmission or other processes; Bayesian inference combines a likelihood with prior information to estimate unknown quantities. Either choice can be combined with compartmental structure. Likewise, randomness in the observation model is distinct from randomness in the underlying epidemic process.

Dehning et al. [9] used Bayesian inference to estimate changes in the spread of COVID-19 in Germany. The inferred change points aligned with the timing of interventions, and the analysis emphasised delays between changes in transmission and their appearance in reported cases. This example connects inference with a substantive question about changing epidemic growth.

A posterior interval expresses uncertainty conditional on the model, likelihood, and priors. It should not be read as encompassing every plausible structural explanation. Nor does a narrower interval automatically demonstrate a better method: increased precision can arise from stronger assumptions. In a comparative assessment, interval width is meaningful alongside sensitivity to those assumptions and evidence about predictive performance.

## 5. Non-pharmaceutical interventions: scenarios and associations

Kucharski et al. [10] modelled individual-level transmission across household, workplace, school, and other settings using UK contact data. They compared testing, isolation, tracing, and distancing scenarios. Under their assumptions, combined isolation and tracing achieved greater transmission reductions than the specified mass random testing strategy or self-isolation alone. The study also considered the number of contacts requiring quarantine, connecting transmission outcomes with implementation demands.

These findings should remain attached to the intervention definitions being compared. They do not establish that every tracing programme outperforms every testing programme. Testing frequency, participation, delays, and the contacts reached by tracing are part of the scenario. Removing those conditions changes the meaning of the comparison.

Badr et al. [11] analysed mobility and case growth in 25 heavily affected US counties. They found an association between reduced mobility and subsequent reductions in case growth, with a delay before changes became apparent. Behavioural changes also preceded some official restrictions. The study provides evidence about the relationship between mobility and epidemic trajectories, while illustrating why policy timing alone does not describe all behavioural change.

Together, these examples support a distinction between a modelled intervention effect and an observed association. A scenario asks what happens if specified mechanisms change. An observational analysis asks how measured quantities vary together. Both can inform an intervention question, but neither should silently be presented as identifying the isolated causal effect of a particular policy. Comparisons across studies should retain the setting, outcome, time horizon, and assumed implementation.

The timing and duration of interventions are separate design choices. Tuite et al. [12] used an age-structured model for Ontario to compare fixed-duration measures with interventions switched on and off according to projected intensive-care occupancy. This links control to health-system capacity rather than a predetermined calendar alone. Ngonghala et al. [13] examined combinations of distancing, quarantine, isolation, and mask use in a model informed by New York State and US data. Their scenarios highlighted the possibility of resurgence after early relaxation and the interaction between intervention components. Neither analysis supplies a context-free duration or compliance threshold for control.

Hellewell et al. [14] considered whether isolation and contact tracing could contain introductions using a stochastic transmission model. Control depended on factors including initial case numbers, tracing probability, isolation delay, and transmission before symptoms. The study's assumption that isolation prevents subsequent transmission is consequential: operational effectiveness cannot be inferred from tracing coverage alone if isolation is delayed or incomplete.

Foncea et al. [15] examined sequential testing of exposed contacts as an alternative to quarantine, with isolation following a positive result. The simulation compared test schedules and types against quarantine strategies with different adherence assumptions. Its contribution is a conditional comparison of expected infectiousness under specified strategies. It should not be presented as a trial demonstrating a universal reduction in transmission or as evidence that testing always replaces quarantine without additional risk.

## 6. Vaccination and the limits of counterfactual estimates

Vaccination introduces several possible model mechanisms, including changes in susceptibility and the risk of severe outcomes. Protection against infection and protection against death should be distinguished because a programme can affect these outcomes differently. The effects of waning immunity also depend on the time horizon and on how loss of protection is represented.

Watson et al. [16] modelled the first year of COVID-19 vaccination across 185 countries and territories. They compared vaccination trajectories with a counterfactual without vaccination, calibrating separately to reported COVID-19 deaths and excess mortality. The estimated deaths averted differed between these mortality inputs. This makes the observation basis of the counterfactual visible: the result is an estimate of an unobserved alternative history, rather than a direct count of prevented deaths.

Ghosh and Ghosh [17] extended an SEIR framework to include asymptomatic infection, waning immunity, vaccination, and control measures, considering Italy, India, and Victoria, Australia. Their scenarios illustrate how vaccination and changing contact patterns can be represented jointly. Quantitative outputs remain conditional on the parameter choices, calibration setting, and mechanisms included.

For a narrative synthesis, the transferable contribution is the comparison of mechanisms and assumptions. A vaccination percentage associated with control in one model should not become a universal threshold. Likewise, a projected epidemic trajectory should not be detached from assumptions about future contact rates, immunity, and implementation.

Giordano et al. [18] coupled a vaccination extension of the SIDARTHE model with a data-based representation of healthcare outcomes in Italy. Their scenarios varied vaccination speed, transmission conditions associated with variants, and the sequencing of restrictions. In this early-rollout setting, retaining interventions could reduce the burden while vaccination accumulated. The assumptions included maintained vaccine effectiveness against variants and negligible reinfection over the scenario horizon. These conditions explain why the conclusions should not be transferred unchanged to later immunity and variant settings.

### 6.1. Variant competition and the time horizon of analysis

Betti et al. [19] used a two-strain model fitted to Ontario case data to examine the emergence of B.1.1.7 and its implications for vaccination efforts. Their scenarios connect variant takeover with ongoing interventions and assumed vaccine protection across strains. The paper illustrates the need to specify which properties of an emerging variant differ from those of the resident strain before interpreting a predicted takeover date.

Ciupeanu et al. [20] developed a two-variant SIRS framework and distinguished long-run dominance or coexistence from the behaviour observed within a single epidemic wave. Their analysis, informed by Canadian variant data, showed the importance of transmissibility advantage while also examining how initial infection numbers influence finite-time outbreak size. This distinction matters when a variant with an eventual competitive advantage starts from a small number of infections: asymptotic dominance does not, by itself, determine its contribution during the observed wave. The model provides a way to separate these questions without treating their time horizons as interchangeable.

### 6.2. Reinfection and threshold behaviour

Wang et al. [21] studied an SEIRE model with reinfection, identifying parameter regimes with backward bifurcation and bistability below a basic reproduction number of one. In that regime, the disease-free and endemic outcomes depend on more than the familiar threshold alone, including initial conditions. This is a mathematical result within a specified model, not empirical proof that all COVID-19 epidemics have the same threshold structure. Read alongside vaccination and variant studies, it demonstrates why conclusions about elimination require explicit immunity and reinfection assumptions.

## 7. Statistical surveillance and count-data models

Population-level statistical models complement mechanistic models by describing measured outcomes without necessarily reconstructing all transmission states. Their adequacy depends on the response being modelled. Counts, proportions, and latent infection trajectories require different observation assumptions and should not be compared as though they were the same target.

Scrucca [22] proposed COVINDEX, derived from a generalised additive beta regression model of test positivity over time, and illustrated it with Italian data. This provides a surveillance indicator based on the proportion of tests yielding positive results. Its interpretation remains tied to the testing process: changes in who is tested or why can affect positivity independently of changes in population prevalence. It therefore complements, rather than automatically replaces, transmission estimates.

Khedhiri [23] compared count time-series models with and without zero inflation using daily COVID-19 deaths in Tunisia. In that application, accounting for excess zeros improved the reported fit and forecast performance. The result supports examining the observation distribution when zeros are frequent; it does not establish that zero-inflated models are preferable for every mortality series. Whether zeros represent low incidence, reporting practices, or a separate process requires contextual assessment.

Murakami and Matsui [24] developed a log-Gaussian approximation for over-dispersed Poisson regression, including extensions with spatial or group effects, and applied it to Japanese COVID-19 data. Their work addresses estimation and computational difficulties in sparse count data. This is a different contribution from adding a biological mechanism to a transmission model: the improvement concerns inference for a specified statistical model. Accordingly, computational stability, explanatory associations, and epidemic forecasting accuracy should be evaluated separately.

These examples broaden the review beyond compartmental dynamics while retaining a common question: how does the model connect its target quantity to the available observations? A useful classification distinguishes the epidemiological task from the mathematical technique, allowing a surveillance or forecasting study to be described without implying that it identifies transmission mechanisms.

## 8. Model updating, control, and forecast evaluation

### 8.1. Assimilating observations and choosing interventions

Ghostine et al. [25] combined an extended SEIR model with an ensemble Kalman filter to update states and parameters from daily Saudi Arabian data. Their experiments assessed short-term predictions and vaccination scenarios. Data assimilation makes updating part of the modelling procedure, so forecast performance concerns the model together with its update rule and incoming data. The ensemble used to represent uncertainty within a filter should also be distinguished from an ensemble of separate forecasting models.

Péni et al. [26] formulated nonlinear model predictive control with constraints for COVID-19 management. Their framework includes discrete intervention levels, logical restrictions, and estimation of unobserved states from hospitalisation information. Simulated control strategies vary with the specified objective and constraints. An optimised intervention is therefore optimal for a defined mathematical problem; the result does not independently validate the assumed intervention costs, feasibility, or epidemiological effects.

### 8.2. Forecast scores and model ensembles

Bosse et al. [27] examined scoring epidemiological forecasts after transforming the predicted and observed counts. Using European COVID-19 Forecast Hub data, they showed that a transformation such as $\log(x+1)$ changes the relative emphasis placed on errors at different incidence levels and can change model rankings under probabilistic scores. The transformation changes the evaluation target; it does not retrospectively improve the underlying predictions. This distinction is important when reviewing claims that one forecasting method performs better than another.

In the January 2024 preprint cited in the thesis, Fox et al. [28] analysed ensemble size and component selection using historical influenza and COVID-19 forecasts. They compared randomly assembled ensembles with selections based on individual or joint historical performance. Larger random ensembles generally reduced variability in performance, while selection based on joint performance explored complementarity between models. Improvements were not uniform across every forecast target. The findings motivate evaluating an ensemble's composition and testing period rather than assuming that more models, or the best individual models, always produce the best combined forecast.

Together, these studies make evaluation an explicit part of the review. Forecasts should be compared for the same outcomes and horizons, using observations withheld from fitting and scores aligned with the intended use. A retrospective comparison remains conditional on its selected locations, periods, and contributing models. These constraints matter when transferring performance claims from one epidemic phase to another.

## 9. Comparative synthesis

Table 1 organises the selected work by the question being asked. The categories overlap: a compartmental model may be stochastic, fitted using statistical inference, and used for intervention scenarios. Treating these features as separate dimensions avoids classifying the same study inconsistently.

| Question and examples | Main contribution | Interpretive check |
|:--|:--|:--|
| What structure is sufficient? Bertozzi et al. [1] | Relates parsimonious models to epidemic questions | Is added complexity supported by the intended use and data? |
| What remains undetected? Ivorra et al. [2]; Kucharski et al. [5] | Links observed data to latent transmission | Which additional information constrains unobserved infection? |
| How does transmission change? Hong and Li [8]; Dehning et al. [9] | Estimates time variation and change points | What assumptions distinguish transmission changes from observation changes? |
| What might interventions achieve? Kucharski et al. [10]; Badr et al. [11] | Examines scenarios and mobility associations | Is the conclusion conditional, associational, or causal? |
| What changes with vaccination? Watson et al. [16]; Ghosh and Ghosh [17]; Giordano et al. [18] | Compares vaccination and immunity scenarios | Which outcome, counterfactual, and immunity assumptions are used? |
| How do variants compete? Betti et al. [19]; Ciupeanu et al. [20] | Separates takeover and finite-time epidemic contributions | Is the conclusion about an observed wave or long-run dynamics? |
| How should observations be modelled? Scrucca [22]; Khedhiri [23]; Murakami and Matsui [24] | Models positivity, excess zeros, and over-dispersion | Does the distribution match the target and reporting process? |
| How should forecasts be compared? Bosse et al. [27]; Fox et al. [28] | Examines scoring scales and ensemble composition | Are the target, horizon, testing period, and score comparable? |

**Table 1.** Questions and interpretive checks for the selected studies. The final column is this review's synthesis, not a formal quality score.

Three distinctions provide a practical framework for reading the literature. First, **fit, forecast, and scenario are different outputs**. Fit measures agreement with observations used in estimation. A forecast concerns data not yet used for fitting. A scenario explores specified conditions, which may never occur. Evidence for one does not automatically validate the others.

Second, **uncertainty has several sources**. Parameter uncertainty concerns unknown values within a model; observation uncertainty concerns the relationship between measured and underlying quantities; structural uncertainty concerns the mechanisms and functional forms chosen. Future behaviour and interventions introduce additional scenario uncertainty. Reporting one interval without identifying what varies can conceal these differences.

Third, **the decision question determines the relevant comparison**. A model intended to estimate hospital demand should be assessed against that target, whereas a model intended to explore mechanisms may be judged partly by whether its assumptions are transparent and its conclusions robust to alternatives. Ranking all models by a single fit statistic would collapse these different purposes.

These distinctions suggest a concise reading procedure: identify the target quantity, inspect how observations connect to it, separate fitted assumptions from externally supplied values, and then ask whether the validation matches the claimed use. This procedure is a proposed interpretive framework, not an empirically validated scoring instrument.

## 10. Limitations

The review is purposive, with a strong emphasis on early-pandemic work and selected later methodological developments. It cannot establish how common particular practices were across the full literature or which model family performed best overall. The existing collection and access to original papers shaped selection. Although the selected publication dates extend to early 2024, the review does not comprehensively address successive variants, hybrid immunity, or the full range of forecasting practice. It also does not validate the classification or summarisation pipeline against a manually labelled reference set.

No models were reimplemented, no forecasts were independently rescored, and no formal risk-of-bias tool was applied. The comparisons therefore concern methodological interpretation rather than a replication-based assessment of accuracy. Broader conclusions about predictive superiority or intervention effectiveness would require a different study design and a larger, systematically assembled evidence base.

## 11. Conclusion

The selected COVID-19 studies demonstrate several uses of transmission models: representing unobserved infection, estimating changing epidemic dynamics, comparing interventions, constructing vaccination counterfactuals, studying variant competition, and evaluating forecasts. Their interpretation depends on the connection between the question, the model, and the evidence. A useful synthesis preserves the conditions attached to each result and distinguishes descriptive fit from predictive or causal claims. For future epidemic modelling, the central methodological lesson is to make assumptions and observation processes explicit and to evaluate outputs against their intended purpose.



## References

1. Bertozzi AL, Franco E, Mohler G, Short MB, Sledge D. The challenges of modeling and forecasting the spread of COVID-19. *Proceedings of the National Academy of Sciences*. 2020;117:16732–16738. [doi:10.1073/pnas.2006520117](https://doi.org/10.1073/pnas.2006520117).

2. Ivorra B, Ferrández MR, Vela-Pérez M, Ramos AM. Mathematical modeling of the spread of the coronavirus disease 2019 (COVID-19) taking into account the undetected infections. The case of China. *Communications in Nonlinear Science and Numerical Simulation*. 2020;88:105303. [doi:10.1016/j.cnsns.2020.105303](https://doi.org/10.1016/j.cnsns.2020.105303).

3. Cooper I, Mondal A, Antonopoulos CG. A SIR model assumption for the spread of COVID-19 in different communities. *Chaos, Solitons & Fractals*. 2020;139:110057. [doi:10.1016/j.chaos.2020.110057](https://doi.org/10.1016/j.chaos.2020.110057).

4. Croccolo F, Roman HE. Spreading of infections on random graphs: a percolation-type model for COVID-19. *Chaos, Solitons & Fractals*. 2020;139:110077. [doi:10.1016/j.chaos.2020.110077](https://doi.org/10.1016/j.chaos.2020.110077).

5. Kucharski AJ, Russell TW, Diamond C, et al. Early dynamics of transmission and control of COVID-19: a mathematical modelling study. *The Lancet Infectious Diseases*. 2020;20:553–558. [doi:10.1016/S1473-3099(20)30144-4](https://doi.org/10.1016/S1473-3099(20)30144-4).

6. Anastassopoulou C, Russo L, Tsakris A, Siettos C. Data-based analysis, modelling and forecasting of the COVID-19 outbreak. *PLOS ONE*. 2020;15:e0230405. [doi:10.1371/journal.pone.0230405](https://doi.org/10.1371/journal.pone.0230405).

7. Watson OJ, Alhaffar M, Mehchy Z, et al. Leveraging community mortality indicators to infer COVID-19 mortality and transmission dynamics in Damascus, Syria. *Nature Communications*. 2021;12:2394. [doi:10.1038/s41467-021-22474-9](https://doi.org/10.1038/s41467-021-22474-9).

8. Hong HG, Li Y. Estimation of time-varying reproduction numbers underlying epidemiological processes: a new statistical tool for the COVID-19 pandemic. *PLOS ONE*. 2020;15:e0236464. [doi:10.1371/journal.pone.0236464](https://doi.org/10.1371/journal.pone.0236464).

9. Dehning J, Zierenberg J, Spitzner FP, et al. Inferring change points in the spread of COVID-19 reveals the effectiveness of interventions. *Science*. 2020;369:eabb9789. [doi:10.1126/science.abb9789](https://doi.org/10.1126/science.abb9789).

10. Kucharski AJ, Klepac P, Conlan AJK, et al. Effectiveness of isolation, testing, contact tracing, and physical distancing on reducing transmission of SARS-CoV-2 in different settings: a mathematical modelling study. *The Lancet Infectious Diseases*. 2020;20:1151–1160. [doi:10.1016/S1473-3099(20)30457-6](https://doi.org/10.1016/S1473-3099(20)30457-6).

11. Badr HS, Du H, Marshall M, Dong E, Squire MM, Gardner LM. Association between mobility patterns and COVID-19 transmission in the USA: a mathematical modelling study. *The Lancet Infectious Diseases*. 2020;20:1247–1254. [doi:10.1016/S1473-3099(20)30553-3](https://doi.org/10.1016/S1473-3099(20)30553-3).

12. Tuite AR, Fisman DN, Greer AL. Mathematical modelling of COVID-19 transmission and mitigation strategies in the population of Ontario, Canada. *CMAJ*. 2020;192:E497–E505. [doi:10.1503/cmaj.200476](https://doi.org/10.1503/cmaj.200476).

13. Ngonghala CN, Iboi E, Eikenberry S, et al. Mathematical assessment of the impact of non-pharmaceutical interventions on curtailing the 2019 novel Coronavirus. *Mathematical Biosciences*. 2020;325:108364. [doi:10.1016/j.mbs.2020.108364](https://doi.org/10.1016/j.mbs.2020.108364).

14. Hellewell J, Abbott S, Gimma A, et al. Feasibility of controlling COVID-19 outbreaks by isolation of cases and contacts. *The Lancet Global Health*. 2020;8:e488–e496. [doi:10.1016/S2214-109X(20)30074-7](https://doi.org/10.1016/S2214-109X(20)30074-7).

15. Foncea P, Mondschein S, Olivares M. Replacing quarantine of COVID-19 contacts with periodic testing is also effective in mitigating the risk of transmission. *Scientific Reports*. 2022;12:3620. [doi:10.1038/s41598-022-07447-2](https://doi.org/10.1038/s41598-022-07447-2).

16. Watson OJ, Barnsley G, Toor J, Hogan AB, Winskill P, Ghani AC. Global impact of the first year of COVID-19 vaccination: a mathematical modelling study. *The Lancet Infectious Diseases*. 2022;22:1293–1302. [doi:10.1016/S1473-3099(22)00320-6](https://doi.org/10.1016/S1473-3099(22)00320-6).

17. Ghosh SK, Ghosh S. A mathematical model for COVID-19 considering waning immunity, vaccination and control measures. *Scientific Reports*. 2023;13:3610. [doi:10.1038/s41598-023-30800-y](https://doi.org/10.1038/s41598-023-30800-y).

18. Giordano G, Colaneri M, Di Filippo A, et al. Modeling vaccination rollouts, SARS-CoV-2 variants and the requirement for non-pharmaceutical interventions in Italy. *Nature Medicine*. 2021;27:993–998. [doi:10.1038/s41591-021-01334-5](https://doi.org/10.1038/s41591-021-01334-5).

19. Betti M, Bragazzi NL, Heffernan JM, Kong J, Raad A. Could a new COVID-19 mutant strain undermine vaccination efforts? A mathematical modelling approach for estimating the spread of B.1.1.7 using Ontario, Canada, as a case study. *Vaccines*. 2021;9:592. [doi:10.3390/vaccines9060592](https://doi.org/10.3390/vaccines9060592).

20. Ciupeanu AS, Varughese M, Roda WC, Han D, Cheng Q, Li MY. Mathematical modeling of the dynamics of COVID-19 variants of concern: asymptotic and finite-time perspectives. *Infectious Disease Modelling*. 2022;7:581–596. [doi:10.1016/j.idm.2022.08.004](https://doi.org/10.1016/j.idm.2022.08.004).

21. Wang S, Wang T, Qi YN, Xu F. Backward bifurcation, basic reinfection number and robustness of a SEIRE epidemic model with reinfection. *arXiv preprint*. 2022; arXiv:2205.07258v1. [Preprint](https://arxiv.org/abs/2205.07258v1).

22. Scrucca L. A COVINDEX based on a GAM beta regression model with an application to the COVID-19 pandemic in Italy. *Statistical Methods & Applications*. 2022;31:881–900. [doi:10.1007/s10260-021-00617-y](https://doi.org/10.1007/s10260-021-00617-y).

23. Khedhiri S. Statistical modeling of COVID-19 deaths with excess zero counts. *Epidemiologic Methods*. 2021;10(S1):20210007. [doi:10.1515/em-2021-0007](https://doi.org/10.1515/em-2021-0007).

24. Murakami D, Matsui T. Improved log-Gaussian approximation for over-dispersed Poisson regression: application to spatial analysis of COVID-19. *PLOS ONE*. 2022;17:e0260836. [doi:10.1371/journal.pone.0260836](https://doi.org/10.1371/journal.pone.0260836).

25. Ghostine R, Gharamti M, Hassrouny S, Hoteit I. An extended SEIR model with vaccination for forecasting the COVID-19 pandemic in Saudi Arabia using an ensemble Kalman filter. *Mathematics*. 2021;9:636. [doi:10.3390/math9060636](https://doi.org/10.3390/math9060636).

26. Péni T, Csutak B, Szederkényi G, Röst G. Nonlinear model predictive control with logic constraints for COVID-19 management. *Nonlinear Dynamics*. 2020;102:1965–1986. [doi:10.1007/s11071-020-05980-1](https://doi.org/10.1007/s11071-020-05980-1).

27. Bosse NI, Abbott S, Cori A, van Leeuwen E, Bracher J, Funk S. Scoring epidemiological forecasts on transformed scales. *PLOS Computational Biology*. 2023;19:e1011393. [doi:10.1371/journal.pcbi.1011393](https://doi.org/10.1371/journal.pcbi.1011393).

28. Fox SJ, Kim M, Meyers LA, Reich NG, Ray EL. Optimizing the number of models included in outbreak forecasting ensembles. *medRxiv preprint*. 2024; version posted 7 January 2024. [doi:10.1101/2024.01.05.24300909](https://doi.org/10.1101/2024.01.05.24300909).
