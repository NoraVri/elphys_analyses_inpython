# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

# cell20160606A -
# cell20160606B - basically a passive bag of shapely membrane
# cell20160606C - nothing much interesting going on, didn't see any fast-events
# cell20160712A -
# cell20160712B -  has a good handful of nice big fastevents in the first ~10min of recording. Very pretty reconstructed morph.
# cell20160713B - didn't see any fast-events; also this would be the cell from hell to analyze for that, with it's large-amplitude and hugely wacky oscillations
# cell20160713D -
# cell20160720A
# cell20160720D
# cell20160720E -  not sure what to make of this one - definitely quite a lot of large-amp events (20mV amp failed APs?) in there, but only a few things that clearly look like fast-events (10-15mV). Mostly doing wacky oscillations with amp up to ~15mV.
# cell20160721B - didn't see any fast-events, and only a few spont. APs. Cell mostly just oscillating extremely whackily throughout
# cell20160721C -  has a dozen or so fast-events (amp 8-10mV, not sure if clear groups) that I could easily see; possibly more are hidden in the 20mV amp oscillations that the neuron is doing most of the time. Has a very pretty reconstructed morph.
# cell20160721F -  has tons of fast-events in the first 3 mins of recording, amp ~6 - 30mV. Not a very nice-looking reconstructed morph.
# cell20160725A - has numerous events but mostly amp < 2mV, saw one example of 6mV. Not oscillating.
# cell20160726A - has a handful of fast-events early on, amp 5-7mV (not sure if in groups)
# cell20160726C - saw exactly 1 fast-event in the data.
# cell20160726E - didn't see any spont. fast-events or APs; cell oscillating throughout in various modes
# cell20160728A - a handful spont.APs but didn't see any fast-events; cell just oscillating, with large amp for the most part
# cell20160728B - tons of spont.APs, but saw only 2 fast-events (6 and 10mV); cell oscillating throughout
# cell20160731A - saw 3 fast-events altogether, all ~5mV
# cell20160731B -  has a dozen or so fast-events, looks like two amplitude groups (4 and 8mV). Not the greatest recording; baselinev all over the place (w/o DC injection).
# cell20160802A - has barely a handful of fastevents early on, mostly just oscillating a lot
# cell20160802C - quite a lot of fast-events (and tons of spont APs); mostly very similar amps though (8 - 10mV), and not the greatest recording overall. OK-looking reconstructed morph, very straight neuron
# cell20160802D - has just one or two fastevents and a single spont AP, mostly just oscillating a lot
# cell20160802E -  saw three amplitudes (3, 8 and 10mV) of fast-events, one or two examples of each. Very nice reconstructed morph. with lots of dendrite

