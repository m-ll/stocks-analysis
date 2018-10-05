#!/usr/bin/python3

import os
import sys
import glob
import shutil
import argparse
from datetime import datetime
from process.company import *
from process.download.download import *
from process.extract.extract import *

# https://graphseobourse.fr/classement-des-entreprises-les-plus-innovantes-du-monde/

#---

# sysco: rendement pas top mais 15% hausse en 5ans
# WALGREENS: rendement pas top / hausse 10% + 5ans / PER bas ? cours baisse dans un creux mais bna prevu en hausse les années suivantes ?
# CARDINAL: chute du titre (trouver pourquoi) / croissance 6% / PER faible / rendement correct (?) ?

# nucor: rendement pas top / croissance baisse mais hausse a 5 ans ? titre qui ne baisse pas

# CLOROX: (wrong dividends) PER sous la moyenne / rendement 3% mais pas top croissance ?

# KIMBERLY: chute du titre / baisse BNA (1 année) ? tout le reste 'bon'



# hcp: voir pourquoi en chute












# https://www.suredividend.com/warren-buffett-stocks/

company_groups = { 
	'owned-eu': [
				  # ISIN			ZoneBourse										Morningstar			YahooFin	Reuters			Finviz	TradingSat			Finances
		cCompany( 'FR0000120578', 'SANOFI', 4698, 'SAN', 							'fra', 'xpar',		'SAN.PA',	'SASY.PA', 		'',		'sanofi', 			'Sanofi' ),
		cCompany( 'FR0000120644', 'DANONE', 4634, 'BN', 							'fra', 'xpar',		'BN.PA',	'DANO.PA', 		'',		'danone', 			'Danone' ),
		cCompany( 'FR0000125486', 'VINCI', 4725, 'DG', 								'fra', 'xpar',		'DG.PA',	'SGEF.PA', 		'',		'vinci', 			'Vinci' ),
		cCompany( 'FR0013269123', 'RUBIS', 37262425, 'RUI', 						'fra', 'xpar',		'RUI.PA',	'RUBF.PA', 		'',		'rubis', 			'Rubis_SCA' ),
		cCompany( 'FR0000120222', 'CNP-ASSURANCES', 4633, 'CNP', 					'fra', 'xpar',		'CNP.PA',	'CNPP.PA', 		'',		'cnp-assurances', 	'CNP_Assurances' ),
		cCompany( 'GB0002875804', 'BRITISH-AMERICAN-TOBACCO', 4001163, 'BATS',		'gbr', 'xlon',		'BATS.L',	'BATS.L', 		'',		'', 				'BAT' ),
		cCompany( 'FR0000130452', 'EIFFAGE', 4638, 'FGR', 							'fra', 'xpar',		'FGR.PA',	'FOUG.PA', 		'',		'eiffage', 			'Eiffage' ),
	],	
	'owned-us': [
		cCompany( 'US7134481081', 'PEPSICO', 39085159, 'PEP', 						'usa', 'xnas',		'PEP',		'PEP.O', 		'PEP',	'', 				'PepsiCo' ),
		cCompany( 'US4523081093', 'ILLINOIS-TOOL-WORKS', 13125, 'ITW', 				'usa', 'xnys',		'ITW',		'ITW.N', 		'ITW',	'', 				'Illinois_Tool_Works' ),
		cCompany( 'US00287Y1091', 'ABBVIE', 12136589, 'ABBV', 						'usa', 'xnys',		'ABBV',		'ABBV.N', 		'ABBV',	'', 				'AbbVie' ),
		cCompany( 'US1912161007', 'COCA-COLA-COMPANY-THE', 4819, 'KO', 				'usa', 'xnys',		'KO',		'KO.N', 		'KO',	'', 				'Coca-Cola' ),
		cCompany( 'US5246601075', 'LEGGETT-PLATT', 13369, 'LEG', 					'usa', 'xnys',		'LEG',		'LEG.N', 		'LEG',	'', 				'LeggettPlatt' ),
		cCompany( 'US3724601055', 'GENUINE-PARTS-COMPANY', 40311101, 'GPC', 		'usa', 'xnys',		'GPC',		'GPC.N', 		'GPC',	'', 				'Genuine_Parts' ),
		cCompany( 'US7427181091', 'PROCTER-GAMBLE-COMPANY', 4838, 'PG', 			'usa', 'xnys',		'PG',		'PG.N', 		'PG',	'', 				'Procter_Gamble' ),
		cCompany( 'US5797802064', 'MCCORMICK-COMPANY', 13556, 'MKC', 				'usa', 'xnys',		'MKC',		'MKC.N', 		'MKC',	'', 				'McCormick' ),
		cCompany( 'US88579Y1010', '3M-COMPANY', 4836, 'MMM', 						'usa', 'xnys',		'MMM',		'MMM.N', 		'MMM',	'', 				'3M' ),
	],	
	
	'to-take-eu': [	
		cCompany( 'FR0000120271', 'TOTAL', 4717, 'FP', 								'fra', 'xpar',		'FP.PA',	'TOTF.PA', 		'',		'total', 			'TOTAL' ),
		cCompany( 'FR0000120503', 'BOUYGUES', 4620, 'EN', 							'fra', 'xpar',		'EN.PA',	'BOUY.PA', 		'',		'bouygues', 		'Bouygues' ),
		cCompany( 'FR0000121014', 'LVMH-MOET-HENNESSY-VUITTO', 4669, 'MC', 			'fra', 'xpar',		'MC.PA',	'LVMH.PA', 		'',		'lvmh', 			'LVMH' ),
		cCompany( 'NL0000009355', 'UNILEVER-NL', 6290, 'UNA', 						'nld', 'xams',		'UNA.AS',	'UNc.AS', 		'',		'',					'Unilever' ),
		cCompany( 'BE0003470755', 'SOLVAY', 5966, 'SOLB', 							'bel', 'xbru',		'SOLB.BR',	'SOLB.BR', 		'',		'solvay', 			'Solvay' ),
	],	
	
	'to-take-us': [	
		cCompany( 'US5486611073', 'LOWE-S-COMPANIES', 13416, 'LOW', 				'usa', 'xnys',		'LOW',		'LOW.N', 		'LOW',	'', 				'Lowes_Companies' ),
		cCompany( 'US00206R1023', 'AT-T', 14324, 'T', 								'usa', 'xnys',		'T',		'T.N', 			'T',	'', 				'AT_T' ),
		cCompany( 'US1941621039', 'COLGATE-PALMOLIVE-COMPANY', 12089, 'CL', 		'usa', 'xnys',		'CL',		'CL.N', 		'CL',	'', 				'Colgate-Palmolive' ),
		cCompany( 'US6703461052', 'NUCOR', 13823, 'NUE', 							'usa', 'xnys',		'NUE',		'NUE.N', 		'NUE',	'', 				'Nucor' ),
	],
	
	#---
	
	'per-too-high-eu': [	
		cCompany( 'FR0000039299', 'BOLLORE', 5155, 'BOL', 							'fra', 'xpar',		'BOL.PA',	'BOLL.PA', 		'',		'bollore', 			'Bollore' ),
		cCompany( 'FR0000052292', 'HERMES-INTERNATIONAL', 4657, 'RMS', 				'fra', 'xpar',		'RMS.PA',	'HRMS.PA', 		'',		'hermes-intl', 		'Hermès' ),
		cCompany( 'FR0000120321', 'L-OREAL', 4666, 'OR', 							'fra', 'xpar',		'OR.PA',	'OREP.PA', 		'',		'loreal', 			'LOréal' ),
		cCompany( 'FR0000184798', 'ORPEA', 4799, 'ORP', 							'fra', 'xpar',		'ORP.PA',	'ORP.PA', 		'',		'orpea', 			'OrpeaAct' ),
		cCompany( 'DE000STRA555', 'STRATEC-BIOMEDICAL-AG', 23566602, 'SBS', 		'deu', 'xetr',		'SBS.DE',	'SBSG.DE', 		'',		'', 				'STRATEC_Biomedical' ),
		cCompany( 'DE0005158703', 'BECHTLE-AG', 435706, 'BC8', 						'deu', 'xetr',		'BC8.DE',	'BC8G.DE', 		'',		'', 				'Bechtle' ),
		cCompany( 'DE000A161N30', 'GRENKE-AG', 22890959, 'GLJ', 					'deu', 'xetr',		'GLJ.DE',	'GLJn.DE', 		'',		'', 				'GRENKE' ),
		cCompany( 'DE0005936124', 'OHB-SE', 450143, 'OHB', 							'deu', 'xetr',		'OHB.DE',	'OHBG.DE', 		'',		'', 				'OHB' ),
	],	
	
	'ratio-versement-dividende-too-high-eu': [	
		cCompany( 'ES0130960018', 'ENAGAS', 409361, 'ENG', 							'', '',				'ENG.MC',	'ENAG.MC', 		'',		'', 				'Enagas' ),
		cCompany( 'LU0088087324', 'SES', 4989, 'SESG', 								'fra', 'xpar',		'SESG.PA',	'SESFd.PA', 	'',		'ses', 				'SES_Global' ),
		cCompany( 'DE0005772206', 'FIELMANN-AG', 436069, 'FIE', 					'deu', 'xetr',		'FIE.DE',	'FIEG.DE', 		'',		'', 				'fielmann' ),
		cCompany( 'DE0006013006', 'HAMBORNER-REIT-AG', 436167, 'HAB', 				'', '',				'HAB.DE',	'HABG.DE', 		'',		'', 				'HAMBORNER_REIT' ),
		cCompany( 'CH0012005267', 'NOVARTIS', 9364983, 'NOVN', 						'', '',				'NOVN.VX',	'NOVNEE.S', 	'',		'', 				'Novartis' ),
		cCompany( 'DE0005501357', 'AXEL-SPRINGER-SE', 447459, 'SPR', 				'', '',				'SPR.DE',	'SPRGn.DE', 	'',		'', 				'axel_springer' ),
		cCompany( 'FR0000125585', 'CASINO-GUICHARD-PERRACHON', 4627, 'CO', 			'fra', 'xpar',		'CO.PA',	'CASP.PA', 		'',		'casino-guichard', 	'Casino_Guichard-Perrachon_et_Cie' ),
		cCompany( 'GB0004544929', 'IMPERIAL-BRANDS', 9590191, 'IMB', 				'gbr', 'xlon',		'IMB.L',	'IMB.L', 		'',		'', 				'Imperial_Brands' ),
		cCompany( 'GB00BH4HKS39', 'VODAFONE-GROUP', 15867071, 'VOD', 				'gbr', 'xlon',		'VOD.L',	'VOD.L', 		'VOD',	'', 				'Vodafone' ),
		cCompany( 'ES0173093024', 'RED-ELECTRICA-DE-ESPA-A', 29688106, 'REE', 		'', '',				'0RI5.IL',	'REE.MC', 		'',		'', 				'Red_Electrica' ),
		cCompany( 'FR0000130213', 'LAGARDERE', 4668, 'MMB', 						'fra', 'xpar',		'MMB.PA',	'LAGA.PA', 		'',		'lagardere-sca', 	'Lagardere_SCA' ),
		cCompany( 'GB0009252882', 'GLAXOSMITHKLINE', 9590199, 'GSK', 				'gbr', 'xlon',		'GSK.L',	'GSK.L', 		'',		'', 				'GlaxoSmithKline' ),
	],	
	
	'ratio-versement-dividende-too-high-us': [	
		cCompany( 'US40414L1098', 'HCP', 12889, 'HCP', 								'usa', 'xnys',		'HCP',		'HCP.N', 		'HCP',	'', 				'HCP' ),
		cCompany( 'US3137472060', 'FEDERAL-REALTY-INVESTMENT', 12673, 'FRT', 		'usa', 'xnys',		'FRT',		'FRT.N', 		'FRT',	'', 				'Federal_Realty_Investment_Trust' ),
		cCompany( 'US6676551046', 'NORTHWEST-NATURAL-GAS-CO', 13845, 'NWN', 		'usa', 'xnys',		'NWN',		'NWN.N', 		'NWN',	'', 				'Northwest_Natural_Gas' ),
	],	
	
	'baisse-action-eu': [	
		cCompany( 'FR0000120966', 'BIC', 4617, 'BB', 								'fra', 'xpar',		'BB.PA',	'BICP.PA', 		'',		'bic', 				'BIC' ),
		cCompany( 'GB00B033F229', 'CENTRICA', 9590112, 'CNA', 						'gbr', 'xlon',		'CNA.L',	'CNA.L', 		'',		'', 				'Centrica' ),
		cCompany( 'GB00BK1PTB77', 'AGGREKO-PLC', 16570411, 'AGK', 					'gbr', 'xlon',		'AGK.L',	'AGGK.L', 		'',		'', 				'Aggreko_2' ),
		cCompany( 'GB0009697037', 'BABCOCK-INTERNATIONAL-GRO', 9583549, 'BAB', 		'gbr', 'xlon',		'BAB.L',	'BAB.L', 		'',		'', 				'Babcock_International' ),
	],	
	
	'baisse-bna-eu': [	
		cCompany( 'DE0006083405', 'HORNBACH-HOLDING-AG-CO', 24446172, 'HBH', 		'deu', 'xetr',		'HBH.DE',	'HBH.DE', 		'',		'', 				'Hornbach' ),
		cCompany( 'DE0006084403', 'HORNBACH-BAUMARKT-AG', 449570, 'HBM', 			'deu', 'xetr',		'HBM.DE',	'HBMG.DE', 		'',		'', 				'HORNBACH_Baumarkt' ),
		cCompany( 'CH0038863350', 'NESTLE', 9365334, 'NESN', 						'', '',				'NESN.VX',	'NESN.S', 		'',		'', 				'Nestle' ),
	],	
	
	'baisse-bna-us': [	
		cCompany( 'US3546131018', 'FRANKLIN-RESOURCES', 11807, 'BEN', 				'usa', 'xnys',		'FTF',		'BEN.N', 		'BEN',	'', 				'Franklin_Resources' ),
	],	
	
	# 'too-bad': [	
		# cCompany( 'DE0005785802', 'FRESENIUS-MEDICAL-CARE', 436087, 'FME',		'', '',				'',			'', 			'',		'',					'Fresenius_Medical_Care' ),	# certaines années, baisse dividende
		
		# cCompany( 'DE0007474041', 'PAUL-HARTMANN-AG', 454872, 'PHH2', 			'', '',				'',			'', 			'',		'', 				'Paul_Hartmann' ),		# pas de table
		# cCompany( 'DE0005706535', 'EUROKAI-GMBH-CO-KGAA', 436054, 'EUK3', 		'', '',				'',			'', 			'',		'', 				'EUROKAI_vz' ),		# table vide (rendement/PER/...)
		# cCompany( 'DE0006069008', 'FROSTA-AG', 436194, 'NLM', 					'', '',				'',			'', 			'',		'', 				'FRoSTA' ),		# pas de table
		# cCompany( 'DE0006048408', 'HENKEL-AG-CO-KGAA', 436183, 'HEN', 			'', '',				'',			'', 			'',		'', 				'Henkel' ),		# pas de table
		# cCompany( 'BE0003604155', 'LOTUS-BAKERIES', 3732293, ' LOTB', 			'', '',				'',			'', 			'',		'lotus-bakeries', 	'Lotus_Bakeries_NV' ),		# table presque vide
		# cCompany( 'GB00B03MM408', 'ROYAL-DUTCH-SHELL-B', 6368, 'RDSB', 			'', '',				'',			'', 			'',		'', 				'Shell_B' ),		# same as A (?)
		# cCompany( 'FR0000130403', 'CHRISTIAN-DIOR-SE', 4629, 'CDI', 				'', '',				'CDI.PA',	'DIOR.PA', 		'',		'christian-dior', 	'Christian_Dior' ),		# table un peu vide
		# cCompany( 'GB0007973794', 'SERCO-GROUP-PLC', 9590148, 'SRP', 				'', '',				'SRP.L',	'SRP.L', 		'',		'', 				'Serco_Group' ),		# no dividends (?)
		# cCompany( 'GB0008847096', 'TESCO', 4000540, 'TSCO', 						'', '',				'TSCO.L',	'TSCO.L', 		'',		'', 				'Tesco' ),		# div cut
		
		# cCompany( 'DE0007170300', 'SCHALTBAU-HOLDING-AG', 436561, 'SLT', 			'', '',				'', 		'',				'',		'', 				'Schaltbau' ),		# div cut
		# cCompany( 'DE000A2GS401', 'SOFTWARE', 37926215, 'SOW', 					'', '',				'',			'', 			'',		'', 				'Software' ),		# div cut
		# cCompany( 'GB00B10RZP78', 'UNILEVER', 9590186, 'ULVR', 					'', '',				'',			'', 			'',		'', 				'Unilever_plc' ),		# div cut
		# cCompany( 'GB0001411924', 'SKY', 9590190, 'SKY', 							'', '',				'',			'', 			'',		'', 				'Sky' ),		# div cut
		
		# cCompany( 'DE0007480204', 'DEUTSCHE-EUROSHOP', 447506, 'DEQ', 			'', '',				'',			'', 			'',		'', 				'deutsche_euroshop' ),		# baisse bna
		
		# cCompany( 'US7244791007', 'PITNEY-BOWES-INC', 13938, 'PBI', 				'', '',				'PBI',		'PBI.N', 		'PBI',	'', 				'Pitney_Bowes' ),		# baisse cours, pas de prevision 2020 (manque une colonne)
		
		
		# cCompany( 'US30779N1054', 'FARMERS-MERCHANTS-BANCO', 34858165, 'FMAO', 	'', '',				'FMAO',		'FMAO.O', 		'FMAO',	'', 				'FarmersMerchants_Bancorp_1' ),		# no data and should be fmcb ...
		# cCompany( 'US7843051043', 'SJW-GROUP', 14403, 'SJW', 						'', '',				'SJW',		'SJW.N', 		'SJW',	'', 				'SJW' ),		# no data
		# cCompany( 'US8905161076', 'TOOTSIE-ROLL-INDUSTRIES', 14650, 'TR', 		'', '',				'TR',		'TR.N', 		'TR',	'', 				'Tootsie_Roll_Industries' ),		# no data
	# ],
	
	'eu': [	
		cCompany( 'FR0000121220', 'SODEXO', 4703, 'SW', 							'fra', 'xpar',		'SW.PA',	'EXHO.PA', 		'',		'sodexo', 			'Sodexo' ),
		cCompany( 'FR0000120073', 'AIR-LIQUIDE', 4605, 'AI', 						'fra', 'xpar',		'AI.PA',	'AIRP.PA', 		'',		'air-liquide', 		'Air_Liquide' ),
		cCompany( 'FR0000121667', 'ESSILOR-INTERNATIONAL', 4641, 'EI', 				'', '',				'EI.PA',	'ESSI.PA', 		'',		'essilor-intl', 	'Essilor' ),
		cCompany( 'DE0007236101', 'SIEMENS', 436605, 'SIE', 						'deu', 'xetr',		'SIE.DE',	'SIEGn.DE', 	'',		'',		 			'Siemens' ),
		cCompany( 'DE000BAY0017', 'BAYER', 436063, 'BAYN', 							'deu', 'xetr',		'BAYN.DE',	'BAYGn.DE', 	'',		'', 				'Bayer' ),
		cCompany( 'DE0006483001', 'LINDE-GROUP-THE', 436357, 'LIN', 				'deu', 'xetr',		'LIN.DE',	'LING.DE', 		'',		'', 				'Linde_6' ),
		cCompany( 'DE000A0D9PT0', 'MTU-AERO-ENGINES', 470192, 'MTX', 				'deu', 'xetr',		'MTX.DE',	'MTXGn.DE', 	'',		'', 				'mtu' ),
		cCompany( 'DE000A0H52F5', 'MVV-ENERGIE-AG', 496746, 'MVV1', 				'deu', 'xetr',		'MVV1.DE',	'MVVGn.DE', 	'',		'', 				'MVV_Energie' ),
		cCompany( 'DE0002457512', 'VIB-VERMOEGEN-AG', 455750, 'VIH', 				'deu', 'xetr',		'VIH.DE',	'VIHG.DE', 		'',		'', 				'VIB_Vermoegen' ),
		cCompany( 'GB00B03MLX29', 'ROYAL-DUTCH-SHELL', 6273, 'RDSA', 				'gbr', 'xlon',		'RDSA.L',	'RDSa.L', 		'',		'',					'Shell' ),
		# cCompany( 'FR0000124711', 'UNIBAIL-RODAMCO', 54289, 'UL', 				'', '',				'UL.AS',	'UNBP.AS', 		'',		'unibail-rodamco', 	'Unibail-Rodamco' ),		# apres la fusion apres westfield
		# cCompany( 'FR0013326246', 'UNIBAIL-R-SE-WFD-UNIBAIL', 43851519, 'URW', 	'nld', 'xams',		'UL.AS',	'URW.AS', 		'',		'', 				'Unibail-Rodamco' ),		# pas de rendement avant 2018, refaire les scripts ...
		cCompany( 'BE0974293251', 'ANHEUSER-BUSCH-INBEV', 31571356, 'ABI', 			'bel', 'xbru',		'ABI.BR',	'ABI.BR', 		'',		'', 				'AB_InBev' ),
		cCompany( 'DE0005194062', 'BAYWA-AG', 435730, 'BYW6', 						'', '',				'BYW6.DE',	'BYWGnx.DE', 	'',		'', 				'BayWa' ),
		cCompany( 'CH0012032048', 'ROCHE-HOLDING-LTD', 9364975, 'ROG', 				'', '',				'RO.SW',	'RO.DE', 		'',		'', 				'Roche' ),
		cCompany( 'GB00B24CGK77', 'RECKITT-BENCKISER', 9590106, 'RB', 				'', '',				'RB.L',		'RB.L', 		'',		'', 				'Reckitt_Benckiser' ),
		cCompany( 'FR0000073298', 'IPSOS', 4663, 'IPS', 							'fra', 'xpar',		'IPS.PA',	'ISOS.PA', 		'',		'ipsos', 			'' ),
		cCompany( 'GB0002374006', 'DIAGEO', 4000514, 'DGE', 						'gbr', 'xlon',		'DGE.L',	'DGE.L', 		'',		'diageo', 			'Diageo' ),
		cCompany( 'DE0005790430', 'FUCHS-PETROLUB-SE', 436097, 'FPE3',				'deu', 'xetr',		'FPE3.DE',	'FPEG_p.DE', 	'',		'', 				'fuchs_petrolub_vz' ),
		cCompany( 'DE0005773303', 'FRAPORT', 450725, 'FRA', 						'deu', 'xetr',		'FRA.DE',	'FRAG.DE', 		'',		'', 				'fraport' ),
		cCompany( 'DE0006048432', 'HENKEL', 436185, 'HEN3', 						'deu', 'xetr',		'HEN3.DE',	'HNKG_p.DE', 	'',		'', 				'Henkel_vz' ),
		cCompany( 'FR0000121709', 'GROUPE-SEB', 4701, 'SK', 						'fra', 'xpar',		'SK.PA',	'SEBF.PA', 		'',		'seb', 				'SEB' ),
		cCompany( 'DE0005785604', 'FRESENIUS', 436083, 'FRE', 						'deu', 'xetr',		'FRE.DE',	'FREG.DE', 		'',		'', 				'Fresenius' ),
		cCompany( 'GB0006731235', 'ASSOCIATED-BRITISH-FOODS', 9583547, 'ABF', 		'gbr', 'xlon',		'ABF.L',	'ABF.L', 		'',		'', 				'Associated_British_Foods' ),
		cCompany( 'GB0000566504', 'BHP-BILLITON-PLC', 4001096, 'BLT', 				'gbr', 'xlon',		'BLT.L',	'BLT.L', 		'',		'', 				'BHP_Billiton' ),
		cCompany( 'GB00B0744B38', 'BUNZL', 4005251, 'BNZL', 						'gbr', 'xlon',		'BNZL.L',	'BNZL.L', 		'',		'', 				'Bunzl' ),
		cCompany( 'GB00B07KD360', 'COBHAM', 4005190, 'COB', 						'gbr', 'xlon',		'COB.L',	'COB.L', 		'',		'', 				'Cobham_1' ),
		cCompany( 'BE0974256852', 'COLRUYT', 5976, 'COLR', 							'bel', 'xbru',		'COLR.BR',	'COLR.BR', 		'',		'', 				'Etablissementen_Franz_Colruyt_NV' ),
		cCompany( 'GB00BD6K4575', 'COMPASS-GROUP-PLC', 35939959, 'CPG', 			'gbr', 'xlon',		'CPG.L',	'CPG.L', 		'',		'', 				'Compass_Group_2' ),
		cCompany( 'BE0003797140', 'GROUPE-BRUXELLES-LAMBERT', 5953, 'GBLB', 		'bel', 'xbru',		'GBLB.BR',	'GBLB.BR', 		'',		'', 				'Groupe_Bruxelles_Lambert' ),
		cCompany( 'GB0031638363', 'INTERTEK-GROUP', 4003872, 'ITRK', 				'gbr', 'xlon',		'ITRK.L',	'ITRK.L', 		'',		'', 				'Intertek' ),
		cCompany( 'GB00BZ4BQC70', 'JOHNSON-MATTHEY-PLC', 25600218, 'JMAT', 			'gbr', 'xlon',		'JMAT.L',	'JMAT.L', 		'',		'', 				'Johnson_Matthey_5' ),
		cCompany( 'IE0004906560', 'KERRY-GROUP-PLC', 1412391, 'KYG.A', 				'', '',				'KRZ.IR',	'KYGa.I', 		'',		'', 				'Kerry_Group' ),
		cCompany( 'CH0012005267', 'NOVARTIS', 9364983, 'NOVN', 						'', '',				'NVS',		'NOVN.S', 		'NVS',	'', 				'Novartis' ),
		cCompany( 'DK0060534915', 'NOVO-NORDISK-A-S', 1412980, 'NOVO B', 			'', '',				'NOVO-B.CO','NOVOb.CO', 	'',		'', 				'Novo_Nordisk' ),
		cCompany( 'DK0060336014', 'NOVOZYMES-A-S', 1412985, 'NZYM B', 				'', '',				'NZYM-B.CO','NZYMb.CO', 	'',		'', 				'Novozymes' ),
		cCompany( 'GB0006776081', 'PEARSON', 4000637, 'PSON', 						'gbr', 'xlon',		'PSON.L',	'PSON.L', 		'PSO',	'', 				'Pearson' ),
		cCompany( 'GB00B8C3BL03', 'THE-SAGE-GROUP-PLC', 13421569, 'SGE', 			'gbr', 'xlon',		'SGE.L',	'SGE.L', 		'',		'', 				'Sage' ),
		cCompany( 'GB0007908733', 'SCOTTISH-AND-SOUTHERN-ENE', 4000881, 'SSE', 		'', '',				'SSE.L',	'SSE.L', 		'',		'', 				'SSE' ),
		cCompany( 'SE0000310336', 'SWEDISH-MATCH', 6492173, 'SWMA', 				'', '',				'SWMA.ST',	'SWMA.ST', 		'',		'', 				'Swedish_Match' ),
		cCompany( 'GB0009465807', 'WEIR-GROUP', 9590176, 'WEIR', 					'gbr', 'xlon',		'WEIR.L',	'WEIR.L', 		'',		'', 				'Weir' ),
		cCompany( 'GB00B1KJJ408', 'WHITBREAD', 4006657, 'WTB', 						'gbr', 'xlon',		'WTB.L',	'WTB.L', 		'',		'', 				'Whitbread' ),
		
		# cCompany( 'ES0111845014', 'ABERTIS-INFRAESTRUCTURAS', 69642, 'ABE', 		'', '',				'ABE.MC',	'ABE.MC', 		'',		'', 				'Abertis' ),	# racheté par ACS, Hochtief et Atlantia
	],	
	
	'us': [
		cCompany( 'US14149Y1082', 'CARDINAL-HEALTH', 11969, 'CAH', 					'usa', 'xnys',		'CAH',		'CAH.N', 		'CAH',		'', 			'Cardinal_Health' ),
		cCompany( 'US9314271084', 'WALGREENS-BOOTS-ALLIANCE', 19356230, 'WBA', 		'usa', 'xnas',		'WBA',		'WBA.O', 		'WBA',		'', 			'Walgreens_Boots_Alliance' ),
		cCompany( 'US30231G1022', 'EXXON-MOBIL-CORPORATION', 4822, 'XOM', 			'usa', 'xnys',		'XOM',		'XOM.N', 		'XOM',		'', 			'ExxonMobil' ),
		cCompany( 'US1667641005', 'CHEVRON-CORPORATION', 12064, 'CVX', 				'usa', 'xnys',		'CVX',		'CVX.N', 		'CVX',		'', 			'Chevron' ),
		cCompany( 'US87612E1064', 'TARGET-CORPORATION', 12291, 'TGT', 				'usa', 'xnys',		'TGT',		'TGT.N', 		'TGT',		'', 			'Target' ),
		cCompany( 'US5801351017', 'MCDONALD-S-CORPORATION', 4833, 'MCD', 			'usa', 'xnys',		'MCD',		'MCD.N', 		'MCD',		'', 			'McDonalds' ),
		cCompany( 'US9311421039', 'WAL-MART-STORES', 4841, 'WMT', 					'usa', 'xnys',		'WMT',		'WMT.N', 		'WMT',		'', 			'Walmart' ),
		cCompany( 'US0394831020', 'ARCHER-DANIELS-MIDLAND-CO', 11533, 'ADM', 		'usa', 'xnys',		'ADM',		'ADM.N', 		'ADM',		'', 			'Archer_Daniels_Midland' ),
		cCompany( 'US1156371007', 'BROWN-FORMAN-CORPORATION', 11815, 'BF.A', 		'usa', 'xnys',		'BF-A',		'BFa.N', 		'BF-A',		'', 			'Brown-Forman_a' ),
		cCompany( 'US1156372096', 'BROWN-FORMAN-CORPORATION', 11816, 'BF.B', 		'usa', 'xnys',		'BF-B',		'BFb.N', 		'BF-B',		'', 			'Brown-Forman_b' ),
		cCompany( 'US4404521001', 'HORMEL-FOODS', 12977, 'HRL', 					'usa', 'xnys',		'HRL',		'HRL.N', 		'HRL',		'', 			'Hormel_Foods' ),
		cCompany( 'US4943681035', 'KIMBERLY-CLARK', 13266, 'KMB', 					'usa', 'xnys',		'KMB',		'KMB.N', 		'KMB',		'', 			'Kimberly-Clark' ),
		cCompany( 'US8718291078', 'SYSCO-CORPORATION', 14540, 'SYY', 				'usa', 'xnys',		'SYY',		'SYY.N', 		'SYY',		'', 			'Sysco' ),
		cCompany( 'US1890541097', 'CLOROX', 12103, 'CLX', 							'usa', 'xnys',		'CLX',		'CLX.N', 		'CLX',		'', 			'Clorox' ),
		cCompany( 'US2910111044', 'EMERSON-ELECTRIC', 12451, 'EMR', 				'usa', 'xnys',		'EMR',		'EMR.N', 		'EMR',		'', 			'Emerson_Electric' ),
		cCompany( 'US2600031080', 'DOVER-CORPORATION', 12331, 'DOV', 				'usa', 'xnys',		'DOV',		'DOV.N', 		'DOV',		'', 			'Dover' ),
		cCompany( 'US3848021040', 'GRAINGER-WW', 12858, 'GWW', 						'usa', 'xnys',		'GWW',		'GWW.N', 		'GWW',		'', 			'Grainger' ),
		cCompany( 'IE00BLS09M33', 'PENTAIR-PLC', 16656327, 'PNR', 					'usa', 'xnys',		'PNR',		'PNR.N', 		'PNR',		'', 			'Pentair_2' ),
		cCompany( 'US8545021011', 'STANLEY-BLACK-DECKER', 14522, 'SWK', 			'usa', 'xnys',		'SWK',		'SWK.N', 		'SWK',		'', 			'Stanley_BlackDecker' ),
		cCompany( 'US1729081059', 'CINTAS-CORPORATION', 4861, 'CTAS', 				'usa', 'xnas',		'CTAS',		'CTAS.O', 		'CTAS',		'', 			'Cintas' ),
		cCompany( 'US78409V1044', 'S-P-GLOBAL-INC', 27377749, 'SPGI', 				'usa', 'xnys',		'SPGI',		'SPGI.N', 		'SPGI',		'', 			'S_P_Global' ),
		cCompany( 'US0010551028', 'AFLAC', 11556, 'AFL', 							'usa', 'xnys',		'AFL',		'AFL.N', 		'AFL',		'', 			'Aflac' ),
		cCompany( 'US74144T1088', 'T-ROWE-PRICE-GROUP', 40311214, 'TROW', 			'usa', 'xnas',		'TROW',		'TROW.O', 		'TROW',		'', 			'T_Rowe_Price_Group' ),
		cCompany( 'US1720621010', 'CINCINNATI-FINANCIAL-CORP', 40311119, 'CINF', 	'usa', 'xnas',		'CINF',		'CINF.O', 		'CINF',		'', 			'Cincinnati_Financial' ),
		cCompany( 'US0758871091', 'BECTON-DICKINSON-AND-COM', 11801, 'BDX', 		'usa', 'xnys',		'BDX',		'BDX.N', 		'BDX',		'', 			'Becton,_DickinsonCo_(BD)' ),
		cCompany( 'IE00BTN1Y115', 'MEDTRONIC-PLC', 20661655, 'MDT', 				'usa', 'xnys',		'MDT',		'MDT.N', 		'MDT',		'', 			'Medtronic_2' ),
		cCompany( 'US0028241000', 'ABBOTT-LABORATORIES', 11506, 'ABT', 				'usa', 'xnys',		'ABT',		'ABT.N', 		'ABT',		'', 			'Abbott_Laboratories' ),
		cCompany( 'US4781601046', 'JOHNSON-JOHNSON', 4832, 'JNJ', 					'usa', 'xnys',		'JNJ',		'JNJ.N', 		'JNJ',		'', 			'JohnsonJohnson' ),
		cCompany( 'US0091581068', 'AIR-PRODUCTS-CHEMICALS', 11666, 'APD', 			'usa', 'xnys',		'APD',		'APD.N', 		'APD',		'', 			'Air_Products_and_Chemicals' ),
		cCompany( 'US6935061076', 'PPG-INDUSTRIES', 14090, 'PPG', 					'usa', 'xnys',		'PPG',		'PPG.N', 		'PPG',		'', 			'PPG_Industries' ),
		cCompany( 'US8243481061', 'SHERWIN-WILLIAMS', 14390, 'SHW', 				'usa', 'xnys',		'SHW',		'SHW.N', 		'SHW',		'', 			'Sherwin-Williams' ),
		cCompany( 'US2788651006', 'ECOLAB', 12399, 'ECL', 							'usa', 'xnys',		'ECL',		'ECL.N', 		'ECL',		'', 			'Ecolab' ),
		cCompany( 'US0530151036', 'AUTOMATIC-DATA-PROCESSING', 11713, 'ADP', 		'usa', 'xnas',		'ADP',		'ADP.O', 		'ADP',		'', 			'Automatic_Data_Processing' ),
		cCompany( 'US2091151041', 'CONEDISON', 12403, 'ED', 						'usa', 'xnys',		'ED',		'ED.N', 		'ED',		'', 			'Consolidated_Edison' ),
		cCompany( 'US0814371052', 'BEMIS-COMPANY-INC', 11875, 'BMS', 				'usa', 'xnys',		'BMS',		'BMS.N', 		'BMS',		'', 			'Bemis' ),
		cCompany( 'CH0044328745', 'CHUBB-LTD', 3860961, 'CB', 						'usa', 'xnys',		'CB',		'CB.N', 		'CB',		'', 			'Chubb_3' ),
		cCompany( 'US9182041080', 'VF-CORPORATION', 14798, 'VFC', 					'usa', 'xnys',		'VFC',		'VFC.N', 		'VFC',		'', 			'VF' ),
		cCompany( 'US8318652091', 'AO-SMITH', 40311155, 'AOS', 						'usa', 'xnys',		'AOS',		'AOS.N', 		'AOS',		'', 			'AO_Smith' ),
		cCompany( 'US7766961061', 'ROPER-TECHNOLOGIES', 14279, 'ROP', 				'usa', 'xnys',		'ROP',		'ROP.N', 		'ROP',		'', 			'Roper_Industries' ),
		cCompany( 'US3695501086', 'GENERAL-DYNAMICS', 12723, 'GD', 					'usa', 'xnys',		'GD',		'GD.N', 		'GD',		'', 			'General_Dynamics' ),
		cCompany( 'US74005P1049', 'PRAXAIR', 14158, 'PX', 							'usa', 'xnys',		'PX',		'PX.N', 		'PX',		'', 			'Praxair' ),
			
		#TODO: only 2 column for estimated 2018/2019 ... -_-	
		# cCompany( 'US8585861003', 'STEPAN-COMPANY', 14335, 'SCL', 				'usa', 'xnys',		'SCL',		'SCL.N', 		'SCL',		'', 			'Stepan' ),
		# cCompany( 'US5138471033', 'LANCASTER-COLONY-CORP', 9843, 'LANC', 			'usa', 'xnas',		'LANC',		'LANC.O', 		'LANC',		'', 			'Lancaster_Colony' ),		# no estimated div
		cCompany( 'US0009571003', 'ABM-INDUSTRIES-INC', 11500, 'ABM', 				'usa', 'xnys',		'ABM',		'ABM.N', 		'ABM',		'', 			'ABM_Industries' ),
		cCompany( 'US6556631025', 'NORDSON-CORPORATION', 10175, 'NDSN', 			'usa', 'xnas',		'NDSN',		'NDSN.O', 		'NDSN',		'', 			'Nordson' ),
		cCompany( 'US7010941042', 'PARKER-HANNIFIN', 40295173, 'PH', 				'usa', 'xnys',		'PH',		'PH.N', 		'PH',		'', 			'Parker_Hannifin' ),
		cCompany( 'US0298991011', 'AMERICAN-STATES-WATER-CO', 11734, 'AWR', 		'usa', 'xnys',		'AWR',		'AWR.N', 		'AWR',		'', 			'American_States_Water' ),
		cCompany( 'US1307881029', 'CALIFORNIA-WATER-SERVICE', 12235, 'CWT', 		'usa', 'xnys',		'CWT',		'CWT.N', 		'CWT',		'', 			'California_Water_Service_Group' ),
		cCompany( 'US92240G1013', 'VECTREN-CORP', 14838, 'VVC', 					'usa', 'xnys',		'VVC',		'VVC.N', 		'VVC',		'', 			'Vectren' ),
	],
	}
			
parser = argparse.ArgumentParser( description='Process group(s).' )
parser.add_argument( 'groups', metavar='Group', nargs='*', help='One (or multiple) group(s) name')
parser.add_argument( '--download', action='store_true', help='Download source' )
parser.add_argument( '--suffix', help='Set suffix of output folder', required=True )
args = parser.parse_args()

if not os.path.exists( "geckodriver" ):
	print( "You need to download 'geckodriver' file and move it next to this file")
	sys.exit()

# Create output directories (_output-xxx and _output-xxx/img)
output_name = '_output-{}'.format( args.suffix )
os.makedirs( output_name, exist_ok=True )
image_name = 'img'
output_image_name = '{}/{}'.format( output_name, image_name )
os.makedirs( output_image_name, exist_ok=True )

# Create input (data) directory (_data-xxx)
data_name = '_data-{}'.format( args.suffix )
os.makedirs( data_name, exist_ok=True )

# Update each company directories
for company_group_name in company_groups:
	for company in company_groups[company_group_name]:
		company.DataDir( data_name )
		company.ImageDir( image_name )

#---

for group_name, company_group in company_groups.items():
	if args.groups and not group_name in args.groups:
		continue
	
	print( 'Group: {}'.format( group_name ) )
	
	if args.download:
		DownloadFinancialsMorningstar( company_group )
		DownloadFinancialsZB( company_group )
		DownloadFinancialsFV( company_group )
		DownloadFinancialsR( company_group )
		DownloadFinancialsYF( company_group )
		DownloadFinancialsB( company_group )
		DownloadSociety( company_group )
		DownloadStockPrice( company_group )
		DownloadDividends( company_group )
		BrowserQuit()
	
	Fill( company_group )
	
	company_group_sorted = sorted( company_group, key=lambda company: company.mYieldCurrent, reverse=True )

	content_html = Extract( company_group_sorted )

	print( 'Write html ...' )
	with open( '{}/{}-[{}].html'.format( output_name, group_name, len( company_group_sorted ) ), 'w' ) as output:
		output.write( content_html )
	
	Clean( company_group )
	
	print( '' )
	
#---

# Copy every images
print( 'Write images ...' )
for file in glob.glob( data_name + '/*.gif' ):
	shutil.copy( file, output_image_name )
