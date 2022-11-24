from .jsm import JSM 
from .mhm import MHM 
from .smile import Smile 
from .green_st import GreenStreetRealty 
from .smith import Smith 
from .bankier import Bankier 
from .wampler import Wampler 
from .jsj import JSJ 
from .bailey import Bailey 
from .ugroup import UniversityGroup
from .roland import Roland 
from .appfolio import * 
from .american_campus import * 


Individual = [
  JSM(),
  MHM(),
  Smile(),
  Roland(),
  GreenStreetRealty(),
  Smith(),
  Bankier(),
  Wampler(),
  JSJ(),
  Bailey(),
  UniversityGroup()
]

AllAgencies = AppFolio + AmericanCampus + Individual