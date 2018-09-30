#!/usr/bin/python3

import os
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
						  # ISIN			ZoneBourse										YahooFin	Reuters		Finviz		TradingSat			Finances				intern
				cCompany( 'FR0000120578', 'SANOFI', 4698, 'SAN', 							'SAN.PA',	'SASY.PA', 		'',		'sanofi', 			'Sanofi', 				'_data', 'img' ),
				cCompany( 'FR0000120644', 'DANONE', 4634, 'BN', 							'BN.PA',	'DANO.PA', 		'',		'danone', 			'Danone', 				'_data', 'img' ),
				cCompany( 'FR0000125486', 'VINCI', 4725, 'DG', 								'DG.PA',	'SGEF.PA', 		'',		'vinci', 			'Vinci', 				'_data', 'img' ),
				cCompany( 'FR0013269123', 'RUBIS', 37262425, 'RUI', 						'RUI.PA',	'RUBF.PA', 		'',		'rubis', 			'Rubis_SCA',			'_data', 'img' ),
				cCompany( 'FR0000120222', 'CNP-ASSURANCES', 4633, 'CNP', 					'CNP.PA',	'CNPP.PA', 		'',		'cnp-assurances', 	'CNP_Assurances', 		'_data', 'img' ),
				cCompany( 'GB0002875804', 'BRITISH-AMERICAN-TOBACCO', 4001163, 'BATS',		'BATS.L',	'BATS.L', 		'',		'', 				'BAT', 					'_data', 'img' ),
				cCompany( 'FR0000130452', 'EIFFAGE', 4638, 'FGR', 							'FGR.PA',	'FOUG.PA', 		'',		'eiffage', 			'Eiffage', 				'_data', 'img' ),
			],	
			'owned-us': [
				cCompany( 'US7134481081', 'PEPSICO', 39085159, 'PEP', 						'PEP',		'PEP.O', 	'PEP',		'', 				'PepsiCo', 				'_data', 'img' ),
				cCompany( 'US4523081093', 'ILLINOIS-TOOL-WORKS', 13125, 'ITW', 				'ITW',		'ITW.N', 	'ITW',		'', 				'Illinois_Tool_Works', 	'_data', 'img' ),
				cCompany( 'US00287Y1091', 'ABBVIE', 12136589, 'ABBV', 						'ABBV',		'ABBV.N', 	'ABBV',		'', 				'AbbVie', 				'_data', 'img' ),
				cCompany( 'US1912161007', 'COCA-COLA-COMPANY-THE', 4819, 'KO', 				'KO',		'KO.N', 	'KO',		'', 				'Coca-Cola', 			'_data', 'img' ),
				cCompany( 'US5246601075', 'LEGGETT-PLATT', 13369, 'LEG', 					'LEG',		'LEG.N', 	'LEG',		'', 				'LeggettPlatt', 		'_data', 'img' ),
				cCompany( 'US3724601055', 'GENUINE-PARTS-COMPANY', 40311101, 'GPC', 		'GPC',		'GPC.N', 	'GPC',		'', 				'Genuine_Parts', 		'_data', 'img' ),
				cCompany( 'US7427181091', 'PROCTER-GAMBLE-COMPANY', 4838, 'PG', 			'PG',		'PG.N', 	'PG',		'', 				'Procter_Gamble', 		'_data', 'img' ),
				cCompany( 'US5797802064', 'MCCORMICK-COMPANY', 13556, 'MKC', 				'MKC',		'MKC.N', 	'MKC',		'', 				'McCormick', 			'_data', 'img' ),
				cCompany( 'US88579Y1010', '3M-COMPANY', 4836, 'MMM', 						'MMM',		'MMM.N', 	'MMM',		'', 				'3M', 					'_data', 'img' ),
			],	
			
			'to-take-eu': [	
				cCompany( 'FR0000120271', 'TOTAL', 4717, 'FP', 								'FP.PA',	'TOTF.PA', 		'',		'total', 			'TOTAL', 				'_data', 'img' ),
				cCompany( 'FR0000120503', 'BOUYGUES', 4620, 'EN', 							'EN.PA',	'BOUY.PA', 		'',		'bouygues', 		'Bouygues', 			'_data', 'img' ),
				cCompany( 'FR0000121014', 'LVMH-MOET-HENNESSY-VUITTO', 4669, 'MC', 			'MC.PA',	'LVMH.PA', 		'',		'lvmh', 			'LVMH', 				'_data', 'img' ),
				cCompany( 'NL0000009355', 'UNILEVER-NL', 6290, 'UNA', 						'UNA.AS',	'UNc.AS', 		'',		'',					'Unilever', 			'_data', 'img' ),
				cCompany( 'BE0003470755', 'SOLVAY', 5966, 'SOLB', 							'SOLB.BR',	'SOLB.BR', 		'',		'solvay', 			'Solvay', 				'_data', 'img' ),
			],	
			
			'to-take-us': [	
				cCompany( 'US5486611073', 'LOWE-S-COMPANIES', 13416, 'LOW', 				'LOW',		'LOW.N', 	'LOW',		'', 				'Lowes_Companies', 		'_data', 'img' ),
				cCompany( 'US00206R1023', 'AT-T', 14324, 'T', 								'T',		'T.N', 		'T',		'', 				'AT_T', 				'_data', 'img' ),
				cCompany( 'US1941621039', 'COLGATE-PALMOLIVE-COMPANY', 12089, 'CL', 			'CL',		'CL.N', 	'CL',		'', 			'Colgate-Palmolive', 			'_data', 'img' ),
				cCompany( 'US6703461052', 'NUCOR', 13823, 'NUE', 								'NUE',		'NUE.N', 	'NUE',		'', 			'Nucor', 						'_data', 'img' ),
			],
			
			#---
			
			'per-too-high-eu': [	
				cCompany( 'FR0000039299', 'BOLLORE', 5155, 'BOL', 							'BOL.PA',		'BOLL.PA', 		'',		'bollore', 		'Bollore', 				'_data', 'img' ),
				cCompany( 'FR0000052292', 'HERMES-INTERNATIONAL', 4657, 'RMS', 				'RMS.PA',		'HRMS.PA', 		'',		'hermes-intl', 	'Hermès', 				'_data', 'img' ),
				cCompany( 'FR0000120321', 'L-OREAL', 4666, 'OR', 							'OR.PA',		'OREP.PA', 		'',		'loreal', 		'LOréal', 				'_data', 'img' ),
				cCompany( 'FR0000184798', 'ORPEA', 4799, 'ORP', 							'ORP.PA',		'ORP.PA', 		'',		'orpea', 		'OrpeaAct', 			'_data', 'img' ),
				cCompany( 'DE000STRA555', 'STRATEC-BIOMEDICAL-AG', 23566602, 'SBS', 		'SBS.DE',		'SBSG.DE', 		'',		'', 			'STRATEC_Biomedical',	'_data', 'img' ),
				cCompany( 'DE0005158703', 'BECHTLE-AG', 435706, 'BC8', 						'BC8.DE',		'BC8G.DE', 		'',		'', 			'Bechtle', 				'_data', 'img' ),
				cCompany( 'DE000A161N30', 'GRENKE-AG', 22890959, 'GLJ', 					'GLJ.DE',		'GLJn.DE', 		'',		'', 			'GRENKE', 				'_data', 'img' ),
				cCompany( 'DE0005936124', 'OHB-SE', 450143, 'OHB', 							'OHB.DE',		'OHBG.DE', 		'',		'', 			'OHB', 					'_data', 'img' ),
			],	
			
			'ratio-versement-dividende-too-high-eu': [	
				cCompany( 'ES0130960018', 'ENAGAS', 409361, 'ENG', 							'ENG.MC',		'ENAG.MC', 		'',		'', 				'Enagas', 				'_data', 'img' ),
				cCompany( 'LU0088087324', 'SES', 4989, 'SESG', 								'SESG.PA',		'SESFd.PA', 	'',		'ses', 				'SES_Global',			'_data', 'img' ),
				cCompany( 'DE0005772206', 'FIELMANN-AG', 436069, 'FIE', 					'FIE.DE',		'FIEG.DE', 		'',		'', 				'fielmann', 			'_data', 'img' ),
				cCompany( 'DE0006013006', 'HAMBORNER-REIT-AG', 436167, 'HAB', 				'HAB.DE',		'HABG.DE', 		'',		'', 				'HAMBORNER_REIT', 		'_data', 'img' ),
				cCompany( 'CH0012005267', 'NOVARTIS', 9364983, 'NOVN', 						'NOVN.VX',		'NOVNEE.S', 	'',		'', 				'Novartis', 			'_data', 'img' ),
				cCompany( 'DE0005501357', 'AXEL-SPRINGER-SE', 447459, 'SPR', 				'SPR.DE',		'SPRGn.DE', 	'',		'', 				'axel_springer', 		'_data', 'img' ),
				cCompany( 'FR0000125585', 'CASINO-GUICHARD-PERRACHON', 4627, 'CO', 			'CO.PA',		'CASP.PA', 		'',		'casino-guichard', 	'Casino_Guichard-Perrachon_et_Cie', 				'_data', 'img' ),
				cCompany( 'GB0004544929', 'IMPERIAL-BRANDS', 9590191, 'IMB', 				'IMB.L',		'IMB.L', 		'',		'', 				'Imperial_Brands', 		'_data', 'img' ),
				cCompany( 'GB00BH4HKS39', 'VODAFONE-GROUP', 15867071, 'VOD', 				'VOD.L',		'VOD.L', 		'VOD',	'', 				'Vodafone',				'_data', 'img' ),
				cCompany( 'ES0173093024', 'RED-ELECTRICA-DE-ESPA-A', 29688106, 'REE', 		'0RI5.IL',		'REE.MC', 		'',		'', 				'Red_Electrica',		'_data', 'img' ),
				cCompany( 'FR0000130213', 'LAGARDERE', 4668, 'MMB', 						'MMB.PA',		'LAGA.PA', 		'',		'lagardere-sca', 	'Lagardere_SCA', 		'_data', 'img' ),
				cCompany( 'GB0009252882', 'GLAXOSMITHKLINE', 9590199, 'GSK', 				'GSK.L',		'GSK.L', 		'',		'', 				'GlaxoSmithKline', 		'_data', 'img' ),
			],	
			
			'ratio-versement-dividende-too-high-us': [	
				cCompany( 'US40414L1098', 'HCP', 12889, 'HCP', 								'HCP',			'HCP.N', 		'HCP',	'', 			'HCP', 					'_data', 'img' ),
				cCompany( 'US3137472060', 'FEDERAL-REALTY-INVESTMENT', 12673, 'FRT', 		'FRT',		'FRT.N', 	'FRT',		'', 				'Federal_Realty_Investment_Trust', 		'_data', 'img' ),
				cCompany( 'US6676551046', 'NORTHWEST-NATURAL-GAS-CO', 13845, 'NWN', 		'NWN',		'NWN.N', 	'NWN',		'', 				'Northwest_Natural_Gas', 		'_data', 'img' ),
			],	
			
			'baisse-action-eu': [	
				cCompany( 'FR0000120966', 'BIC', 4617, 'BB', 								'BB.PA',		'BICP.PA', 		'',		'bic', 			'BIC', 					'_data', 'img' ),
				cCompany( 'GB00B033F229', 'CENTRICA', 9590112, 'CNA', 						'CNA.L',		'CNA.L', 		'',		'', 			'Centrica', 			'_data', 'img' ),
				cCompany( 'GB00BK1PTB77', 'AGGREKO-PLC', 16570411, 'AGK', 					'AGK.L',		'AGGK.L', 		'',		'', 			'Aggreko_2', 			'_data', 'img' ),
				cCompany( 'GB0009697037', 'BABCOCK-INTERNATIONAL-GRO', 9583549, 'BAB', 		'BAB.L',		'BAB.L', 		'',		'', 			'Babcock_International', 		'_data', 'img' ),
			],	
			
			'baisse-bna-eu': [	
				cCompany( 'DE0006083405', 'HORNBACH-HOLDING-AG-CO', 24446172, 'HBH', 		'HBH.DE',		'HBH.DE', 		'',		'', 			'Hornbach', 			'_data', 'img' ),
				cCompany( 'DE0006084403', 'HORNBACH-BAUMARKT-AG', 449570, 'HBM', 			'HBM.DE',		'HBMG.DE', 		'',		'', 			'HORNBACH_Baumarkt', 	'_data', 'img' ),
				cCompany( 'CH0038863350', 'NESTLE', 9365334, 'NESN', 						'NESN.VX',		'NESN.S', 		'',		'', 			'Nestle', 				'_data', 'img' ),
			],	
			
			'baisse-bna-us': [	
				cCompany( 'US3546131018', 'FRANKLIN-RESOURCES', 11807, 'BEN', 				'FTF',			'BEN.N', 		'BEN',	'', 				'Franklin_Resources',	'_data', 'img' ),
			],	
			
			# 'too-bad': [	
				# cCompany( 'DE0005785802', 'FRESENIUS-MEDICAL-CARE', 436087, 'FME',		'',		'', 		'',		'',					'Fresenius_Medical_Care', '_data', 'img' ),	# certaines années, baisse dividende
				
				# cCompany( 'DE0007474041', 'PAUL-HARTMANN-AG', 454872, 'PHH2', 			'',		'', 		'',		'', 				'Paul_Hartmann', 		'_data', 'img' ),		# pas de table
				# cCompany( 'DE0005706535', 'EUROKAI-GMBH-CO-KGAA', 436054, 'EUK3', 		'',		'', 		'',		'', 				'EUROKAI_vz', 			'_data', 'img' ),		# table vide (rendement/PER/...)
				# cCompany( 'DE0006069008', 'FROSTA-AG', 436194, 'NLM', 					'',		'', 		'',		'', 				'FRoSTA', 				'_data', 'img' ),		# pas de table
				# cCompany( 'DE0006048408', 'HENKEL-AG-CO-KGAA', 436183, 'HEN', 			'',		'', 		'',		'', 				'Henkel', 				'_data', 'img' ),		# pas de table
				# cCompany( 'BE0003604155', 'LOTUS-BAKERIES', 3732293, ' LOTB', 			'',		'', 		'',		'lotus-bakeries', 	'Lotus_Bakeries_NV',	'_data', 'img' ),		# table presque vide
				# cCompany( 'GB00B03MM408', 'ROYAL-DUTCH-SHELL-B', 6368, 'RDSB', 			'',		'', 		'',		'', 				'Shell_B', 				'_data', 'img' ),		# same as A (?)
				# cCompany( 'FR0000130403', 'CHRISTIAN-DIOR-SE', 4629, 'CDI', 				'CDI.PA',	'DIOR.PA', 		'',		'christian-dior', 	'Christian_Dior', 		'_data', 'img' ),		# table un peu vide
				# cCompany( 'GB0007973794', 'SERCO-GROUP-PLC', 9590148, 'SRP', 				'SRP.L',	'SRP.L', 		'',		'', 				'Serco_Group',			'_data', 'img' ),		# no dividends (?)
				# cCompany( 'GB0008847096', 'TESCO', 4000540, 'TSCO', 						'TSCO.L',	'TSCO.L', 		'',		'', 				'Tesco',				'_data', 'img' ),		# div cut
				
				# cCompany( 'DE0007170300', 'SCHALTBAU-HOLDING-AG', 436561, 'SLT', 			'',		'', 		'',		'', 				'Schaltbau', 			'_data', 'img' ),		# div cut
				# cCompany( 'DE000A2GS401', 'SOFTWARE', 37926215, 'SOW', 					'',		'', 		'',		'', 				'Software', 			'_data', 'img' ),		# div cut
				# cCompany( 'GB00B10RZP78', 'UNILEVER', 9590186, 'ULVR', 					'',		'', 		'',		'', 				'Unilever_plc', 		'_data', 'img' ),		# div cut
				# cCompany( 'GB0001411924', 'SKY', 9590190, 'SKY', 							'',		'', 		'',		'', 				'Sky', 					'_data', 'img' ),		# div cut
				
				# cCompany( 'DE0007480204', 'DEUTSCHE-EUROSHOP', 447506, 'DEQ', 				'',		'', 		'',		'', 				'deutsche_euroshop', 	'_data', 'img' ),		# baisse bna
				
				# cCompany( 'US7244791007', 'PITNEY-BOWES-INC', 13938, 'PBI', 				'PBI',	'PBI.N', 		'PBI',		'', 				'Pitney_Bowes', 		'_data', 'img' ),		# baisse cours, pas de prevision 2020 (manque une colonne)
				
				
				# cCompany( 'US30779N1054', 'FARMERS-MERCHANTS-BANCO', 34858165, 'FMAO', 		'FMAO',		'FMAO.O', 	'FMAO',		'', 				'FarmersMerchants_Bancorp_1', 	'_data', 'img' ),		# no data and should be fmcb ...
				# cCompany( 'US7843051043', 'SJW-GROUP', 14403, 'SJW', 						'SJW',		'SJW.N', 	'SJW',		'', 				'SJW', 					'_data', 'img' ),		# no data
				# cCompany( 'US8905161076', 'TOOTSIE-ROLL-INDUSTRIES', 14650, 'TR', 			'TR',		'TR.N', 	'TR',		'', 				'Tootsie_Roll_Industries', 	'_data', 'img' ),		# no data
			# ],
			
			'eu': [	
				cCompany( 'FR0000121220', 'SODEXO', 4703, 'SW', 							'SW.PA',	'EXHO.PA', 		'',		'sodexo', 			'Sodexo', 				'_data', 'img' ),
				cCompany( 'FR0000120073', 'AIR-LIQUIDE', 4605, 'AI', 						'AI.PA',	'AIRP.PA', 		'',		'air-liquide', 		'Air_Liquide', 			'_data', 'img' ),
				cCompany( 'FR0000121667', 'ESSILOR-INTERNATIONAL', 4641, 'EI', 				'EI.PA',	'ESSI.PA', 		'',		'essilor-intl', 	'Essilor', 				'_data', 'img' ),
				cCompany( 'DE0007236101', 'SIEMENS', 436605, 'SIE', 						'SIE.DE',	'SIEGn.DE', 	'',		'',		 			'Siemens', 				'_data', 'img' ),
				cCompany( 'DE000BAY0017', 'BAYER', 436063, 'BAYN', 							'BAYN.DE',	'BAYGn.DE', 	'',		'', 				'Bayer', 				'_data', 'img' ),
				cCompany( 'DE0006483001', 'LINDE-GROUP-THE', 436357, 'LIN', 				'LIN.DE',	'LING.DE', 		'',		'', 				'Linde_6', 				'_data', 'img' ),
				cCompany( 'DE000A0D9PT0', 'MTU-AERO-ENGINES', 470192, 'MTX', 				'MTX.DE',	'MTXGn.DE', 	'',		'', 				'mtu', 					'_data', 'img' ),
				cCompany( 'DE000A0H52F5', 'MVV-ENERGIE-AG', 496746, 'MVV1', 				'MVV1.DE',	'MVVGn.DE', 	'',		'', 				'MVV_Energie', 			'_data', 'img' ),
				cCompany( 'DE0002457512', 'VIB-VERMOEGEN-AG', 455750, 'VIH', 				'VIH.DE',	'VIHG.DE', 		'',		'', 				'VIB_Vermoegen', 		'_data', 'img' ),
				cCompany( 'GB00B03MLX29', 'ROYAL-DUTCH-SHELL', 6273, 'RDSA', 				'RDSA.L',	'RDSa.L', 		'',		'',					'Shell', 		 		'_data', 'img' ),
				# cCompany( 'FR0000124711', 'UNIBAIL-RODAMCO', 54289, 'UL', 					'UL.AS',	'UNBP.AS', 		'',		'unibail-rodamco', 	'Unibail-Rodamco', 		'_data', 'img' ),		# apres la fusion apres westfield
				# cCompany( 'FR0013326246', 'UNIBAIL-R-SE-WFD-UNIBAIL', 43851519, 'URW', 		'UL.AS',	'URW.AS', 		'',		'', 				'Unibail-Rodamco', 		'_data', 'img' ),		# pas de rendement avant 2018, refaire les scripts ...
				cCompany( 'BE0974293251', 'ANHEUSER-BUSCH-INBEV', 31571356, 'ABI', 			'ABI.BR',	'ABI.BR', 		'',		'', 				'AB_InBev', 			'_data', 'img' ),
				cCompany( 'DE0005194062', 'BAYWA-AG', 435730, 'BYW6', 						'BYW6.DE',	'BYWGnx.DE', 	'',		'', 				'BayWa', 				'_data', 'img' ),
				cCompany( 'CH0012032048', 'ROCHE-HOLDING-LTD', 9364975, 'ROG', 				'RO.SW',	'RO.DE', 		'',		'', 				'Roche', 				'_data', 'img' ),
				cCompany( 'GB00B24CGK77', 'RECKITT-BENCKISER', 9590106, 'RB', 				'RB.L',		'RB.L', 		'',		'', 				'Reckitt_Benckiser', 	'_data', 'img' ),
				cCompany( 'FR0000073298', 'IPSOS', 4663, 'IPS', 							'IPS.PA',	'ISOS.PA', 		'',		'ipsos', 			'', 					'_data', 'img' ),
				cCompany( 'GB0002374006', 'DIAGEO', 4000514, 'DGE', 						'DGE.L',	'DGE.L', 		'',		'diageo', 			'Diageo', 				'_data', 'img' ),
				cCompany( 'DE0005790430', 'FUCHS-PETROLUB-SE', 436097, 'FPE3',				'FPE3.DE',	'FPEG_p.DE', 	'',		'', 				'fuchs_petrolub_vz', 	'_data', 'img' ),
				cCompany( 'DE0005773303', 'FRAPORT', 450725, 'FRA', 						'FRA.DE',	'FRAG.DE', 		'',		'', 				'fraport', 				'_data', 'img' ),
				cCompany( 'DE0006048432', 'HENKEL', 436185, 'HEN3', 						'HEN3.DE',	'HNKG_p.DE', 	'',		'', 				'Henkel_vz', 			'_data', 'img' ),
				cCompany( 'FR0000121709', 'GROUPE-SEB', 4701, 'SK', 						'SK.PA',	'SEBF.PA', 		'',		'seb', 				'SEB',		 			'_data', 'img' ),
				cCompany( 'DE0005785604', 'FRESENIUS', 436083, 'FRE', 						'FRE.DE',	'FREG.DE', 		'',		'', 				'Fresenius',			'_data', 'img' ),
				cCompany( 'GB0006731235', 'ASSOCIATED-BRITISH-FOODS', 9583547, 'ABF', 		'ABF.L',	'ABF.L', 		'',		'', 				'Associated_British_Foods', 	'_data', 'img' ),
				cCompany( 'GB0000566504', 'BHP-BILLITON-PLC', 4001096, 'BLT', 				'BLT.L',	'BLT.L', 		'',		'', 				'BHP_Billiton', 		'_data', 'img' ),
				cCompany( 'GB00B0744B38', 'BUNZL', 4005251, 'BNZL', 						'BNZL.L',	'BNZL.L', 		'',		'', 				'Bunzl', 				'_data', 'img' ),
				cCompany( 'GB00B07KD360', 'COBHAM', 4005190, 'COB', 						'COB.L',	'COB.L', 		'',		'', 				'Cobham_1', 			'_data', 'img' ),
				cCompany( 'BE0974256852', 'COLRUYT', 5976, 'COLR', 							'COLR.BR',	'COLR.BR', 		'',		'', 				'Etablissementen_Franz_Colruyt_NV', '_data', 'img' ),
				cCompany( 'GB00BD6K4575', 'COMPASS-GROUP-PLC', 35939959, 'CPG', 			'CPG.L',	'CPG.L', 		'',		'', 				'Compass_Group_2', 		'_data', 'img' ),
				cCompany( 'BE0003797140', 'GROUPE-BRUXELLES-LAMBERT', 5953, 'GBLB', 		'GBLB.BR',	'GBLB.BR', 		'',		'', 				'Groupe_Bruxelles_Lambert', 		'_data', 'img' ),
				cCompany( 'GB0031638363', 'INTERTEK-GROUP', 4003872, 'ITRK', 				'ITRK.L',	'ITRK.L', 		'',		'', 				'Intertek', 			'_data', 'img' ),
				cCompany( 'GB00BZ4BQC70', 'JOHNSON-MATTHEY-PLC', 25600218, 'JMAT', 			'JMAT.L',	'JMAT.L', 		'',		'', 				'Johnson_Matthey_5', 	'_data', 'img' ),
				cCompany( 'IE0004906560', 'KERRY-GROUP-PLC', 1412391, 'KYG.A', 				'KRZ.IR',	'KYGa.I', 		'',		'', 				'Kerry_Group', 			'_data', 'img' ),
				cCompany( 'CH0012005267', 'NOVARTIS', 9364983, 'NOVN', 						'NVS',		'NOVN.S', 		'NVS',	'', 				'Novartis', 			'_data', 'img' ),
				cCompany( 'DK0060534915', 'NOVO-NORDISK-A-S', 1412980, 'NOVO B', 			'NOVO-B.CO','NOVOb.CO', 	'',		'', 				'Novo_Nordisk', 		'_data', 'img' ),
				cCompany( 'DK0060336014', 'NOVOZYMES-A-S', 1412985, 'NZYM B', 				'NZYM-B.CO','NZYMb.CO', 	'',		'', 				'Novozymes', 			'_data', 'img' ),
				cCompany( 'GB0006776081', 'PEARSON', 4000637, 'PSON', 						'PSON.L',	'PSON.L', 		'PSO',	'', 				'Pearson', 				'_data', 'img' ),
				cCompany( 'GB00B8C3BL03', 'THE-SAGE-GROUP-PLC', 13421569, 'SGE', 			'SGE.L',	'SGE.L', 		'',		'', 				'Sage',					'_data', 'img' ),
				cCompany( 'GB0007908733', 'SCOTTISH-AND-SOUTHERN-ENE', 4000881, 'SSE', 		'SSE.L',	'SSE.L', 		'',		'', 				'SSE',					'_data', 'img' ),
				cCompany( 'SE0000310336', 'SWEDISH-MATCH', 6492173, 'SWMA', 				'SWMA.ST',	'SWMA.ST', 		'',		'', 				'Swedish_Match',		'_data', 'img' ),
				cCompany( 'GB0009465807', 'WEIR-GROUP', 9590176, 'WEIR', 					'WEIR.L',	'WEIR.L', 		'',		'', 				'Weir',					'_data', 'img' ),
				cCompany( 'GB00B1KJJ408', 'WHITBREAD', 4006657, 'WTB', 						'WTB.L',	'WTB.L', 		'',		'', 				'Whitbread',			'_data', 'img' ),
				
				# cCompany( 'ES0111845014', 'ABERTIS-INFRAESTRUCTURAS', 69642, 'ABE', 		'ABE.MC',	'ABE.MC', 		'',		'', 				'Abertis', 				'_data', 'img' ),	# racheté par ACS, Hochtief et Atlantia
			],	
			
			'us': [
				cCompany( 'US14149Y1082', 'CARDINAL-HEALTH', 11969, 'CAH', 					'CAH',		'CAH.N', 	'CAH',		'', 				'Cardinal_Health', 		'_data', 'img' ),
				cCompany( 'US9314271084', 'WALGREENS-BOOTS-ALLIANCE', 19356230, 'WBA', 			'WBA',		'WBA.O', 	'WBA',		'', 			'Walgreens_Boots_Alliance', 	'_data', 'img' ),
				cCompany( 'US30231G1022', 'EXXON-MOBIL-CORPORATION', 4822, 'XOM', 				'XOM',		'XOM.N', 	'XOM',		'', 			'ExxonMobil', 					'_data', 'img' ),
				cCompany( 'US1667641005', 'CHEVRON-CORPORATION', 12064, 'CVX', 					'CVX',		'CVX.N', 	'CVX',		'', 			'Chevron', 						'_data', 'img' ),
				cCompany( 'US87612E1064', 'TARGET-CORPORATION', 12291, 'TGT', 					'TGT',		'TGT.N', 	'TGT',		'', 			'Target', 						'_data', 'img' ),
				cCompany( 'US5801351017', 'MCDONALD-S-CORPORATION', 4833, 'MCD', 				'MCD',		'MCD.N', 	'MCD',		'', 			'McDonalds', 					'_data', 'img' ),
				cCompany( 'US9311421039', 'WAL-MART-STORES', 4841, 'WMT', 						'WMT',		'WMT.N', 	'WMT',		'', 			'Walmart', 						'_data', 'img' ),
				cCompany( 'US0394831020', 'ARCHER-DANIELS-MIDLAND-CO', 11533, 'ADM', 			'ADM',		'ADM.N', 	'ADM',		'', 			'Archer_Daniels_Midland', 		'_data', 'img' ),
				cCompany( 'US1156371007', 'BROWN-FORMAN-CORPORATION', 11815, 'BF.A', 			'BF-A',		'BFa.N', 	'BF-A',		'', 			'Brown-Forman_a', 				'_data', 'img' ),
				cCompany( 'US1156372096', 'BROWN-FORMAN-CORPORATION', 11816, 'BF.B', 			'BF-B',		'BFb.N', 	'BF-B',		'', 			'Brown-Forman_b', 				'_data', 'img' ),
				cCompany( 'US4404521001', 'HORMEL-FOODS', 12977, 'HRL', 						'HRL',		'HRL.N', 	'HRL',		'', 			'Hormel_Foods', 				'_data', 'img' ),
				cCompany( 'US4943681035', 'KIMBERLY-CLARK', 13266, 'KMB', 						'KMB',		'KMB.N', 	'KMB',		'', 			'Kimberly-Clark', 				'_data', 'img' ),
				cCompany( 'US8718291078', 'SYSCO-CORPORATION', 14540, 'SYY', 					'SYY',		'SYY.N', 	'SYY',		'', 			'Sysco', 						'_data', 'img' ),
				cCompany( 'US1890541097', 'CLOROX', 12103, 'CLX', 								'CLX',		'CLX.N', 	'CLX',		'', 			'Clorox', 						'_data', 'img' ),
				cCompany( 'US2910111044', 'EMERSON-ELECTRIC', 12451, 'EMR', 					'EMR',		'EMR.N', 	'EMR',		'', 			'Emerson_Electric', 			'_data', 'img' ),
				cCompany( 'US2600031080', 'DOVER-CORPORATION', 12331, 'DOV', 					'DOV',		'DOV.N', 	'DOV',		'', 			'Dover', 						'_data', 'img' ),
				cCompany( 'US3848021040', 'GRAINGER-WW', 12858, 'GWW', 							'GWW',		'GWW.N', 	'GWW',		'', 			'Grainger', 					'_data', 'img' ),
				cCompany( 'IE00BLS09M33', 'PENTAIR-PLC', 16656327, 'PNR', 						'PNR',		'PNR.N', 	'PNR',		'', 			'Pentair_2', 					'_data', 'img' ),
				cCompany( 'US8545021011', 'STANLEY-BLACK-DECKER', 14522, 'SWK', 				'SWK',		'SWK.N', 	'SWK',		'', 			'Stanley_BlackDecker', 			'_data', 'img' ),
				cCompany( 'US1729081059', 'CINTAS-CORPORATION', 4861, 'CTAS', 					'CTAS',		'CTAS.O', 	'CTAS',		'', 			'Cintas', 						'_data', 'img' ),
				cCompany( 'US78409V1044', 'S-P-GLOBAL-INC', 27377749, 'SPGI', 					'SPGI',		'SPGI.N', 	'SPGI',		'', 			'S_P_Global', 					'_data', 'img' ),
				cCompany( 'US0010551028', 'AFLAC', 11556, 'AFL', 								'AFL',		'AFL.N', 	'AFL',		'', 			'Aflac', 						'_data', 'img' ),
				cCompany( 'US74144T1088', 'T-ROWE-PRICE-GROUP', 40311214, 'TROW', 				'TROW',		'TROW.O', 	'TROW',		'', 			'T_Rowe_Price_Group', 			'_data', 'img' ),
				cCompany( 'US1720621010', 'CINCINNATI-FINANCIAL-CORP', 40311119, 'CINF', 		'CINF',		'CINF.O', 	'CINF',		'', 			'Cincinnati_Financial', 		'_data', 'img' ),
				cCompany( 'US0758871091', 'BECTON-DICKINSON-AND-COM', 11801, 'BDX', 			'BDX',		'BDX.N', 	'BDX',		'', 			'Becton,_DickinsonCo_(BD)', 	'_data', 'img' ),
				cCompany( 'IE00BTN1Y115', 'MEDTRONIC-PLC', 20661655, 'MDT', 					'MDT',		'MDT.N', 	'MDT',		'', 			'Medtronic_2', 					'_data', 'img' ),
				cCompany( 'US0028241000', 'ABBOTT-LABORATORIES', 11506, 'ABT', 					'ABT',		'ABT.N', 	'ABT',		'', 			'Abbott_Laboratories', 			'_data', 'img' ),
				cCompany( 'US4781601046', 'JOHNSON-JOHNSON', 4832, 'JNJ', 						'JNJ',		'JNJ.N', 	'JNJ',		'', 			'JohnsonJohnson', 				'_data', 'img' ),
				cCompany( 'US0091581068', 'AIR-PRODUCTS-CHEMICALS', 11666, 'APD', 				'APD',		'APD.N', 	'APD',		'', 			'Air_Products_and_Chemicals', 	'_data', 'img' ),
				cCompany( 'US6935061076', 'PPG-INDUSTRIES', 14090, 'PPG', 						'PPG',		'PPG.N', 	'PPG',		'', 			'PPG_Industries', 				'_data', 'img' ),
				cCompany( 'US8243481061', 'SHERWIN-WILLIAMS', 14390, 'SHW', 					'SHW',		'SHW.N', 	'SHW',		'', 			'Sherwin-Williams', 			'_data', 'img' ),
				cCompany( 'US2788651006', 'ECOLAB', 12399, 'ECL', 								'ECL',		'ECL.N', 	'ECL',		'', 			'Ecolab', 						'_data', 'img' ),
				cCompany( 'US0530151036', 'AUTOMATIC-DATA-PROCESSING', 11713, 'ADP', 			'ADP',		'ADP.O', 	'ADP',		'', 			'Automatic_Data_Processing', 	'_data', 'img' ),
				cCompany( 'US2091151041', 'CONEDISON', 12403, 'ED', 							'ED',		'ED.N', 	'ED',		'', 			'Consolidated_Edison', 			'_data', 'img' ),
				cCompany( 'US0814371052', 'BEMIS-COMPANY-INC', 11875, 'BMS', 					'BMS',		'BMS.N', 	'BMS',		'', 			'Bemis', 						'_data', 'img' ),
				cCompany( 'CH0044328745', 'CHUBB-LTD', 3860961, 'CB', 							'CB',		'CB.N', 	'CB',		'', 			'Chubb_3', 						'_data', 'img' ),
				cCompany( 'US9182041080', 'VF-CORPORATION', 14798, 'VFC', 						'VFC',		'VFC.N', 	'VFC',		'', 			'VF', 							'_data', 'img' ),
				cCompany( 'US8318652091', 'AO-SMITH', 40311155, 'AOS', 							'AOS',		'AOS.N', 	'AOS',		'', 			'AO_Smith', 					'_data', 'img' ),
				cCompany( 'US7766961061', 'ROPER-TECHNOLOGIES', 14279, 'ROP', 					'ROP',		'ROP.N', 	'ROP',		'', 			'Roper_Industries', 			'_data', 'img' ),
				cCompany( 'US3695501086', 'GENERAL-DYNAMICS', 12723, 'GD', 						'GD',		'GD.N', 	'GD',		'', 			'General_Dynamics', 			'_data', 'img' ),
				cCompany( 'US74005P1049', 'PRAXAIR', 14158, 'PX', 								'PX',		'PX.N', 	'PX',		'', 			'Praxair', 						'_data', 'img' ),
				
				#TODO: only 2 column for estimated 2018/2019 ... -_-
				# cCompany( 'US8585861003', 'STEPAN-COMPANY', 14335, 'SCL', 					'SCL',		'SCL.N', 	'SCL',		'', 			'Stepan', 						'_data', 'img' ),
				# cCompany( 'US5138471033', 'LANCASTER-COLONY-CORP', 9843, 'LANC', 				'LANC',		'LANC.O', 	'LANC',		'', 			'Lancaster_Colony', 			'_data', 'img' ),		# no estimated div
				cCompany( 'US0009571003', 'ABM-INDUSTRIES-INC', 11500, 'ABM', 					'ABM',		'ABM.N', 	'ABM',		'', 			'ABM_Industries', 				'_data', 'img' ),
				cCompany( 'US6556631025', 'NORDSON-CORPORATION', 10175, 'NDSN', 				'NDSN',		'NDSN.O', 	'NDSN',		'', 			'Nordson', 						'_data', 'img' ),
				cCompany( 'US7010941042', 'PARKER-HANNIFIN', 40295173, 'PH', 					'PH',		'PH.N', 	'PH',		'', 			'Parker_Hannifin', 				'_data', 'img' ),
				cCompany( 'US0298991011', 'AMERICAN-STATES-WATER-CO', 11734, 'AWR', 			'AWR',		'AWR.N', 	'AWR',		'', 			'American_States_Water', 		'_data', 'img' ),
				cCompany( 'US1307881029', 'CALIFORNIA-WATER-SERVICE', 12235, 'CWT', 			'CWT',		'CWT.N', 	'CWT',		'', 			'California_Water_Service_Group', 	'_data', 'img' ),
				cCompany( 'US92240G1013', 'VECTREN-CORP', 14838, 'VVC', 						'VVC',		'VVC.N', 	'VVC',		'', 			'Vectren', 						'_data', 'img' ),
			],
			}
			
parser = argparse.ArgumentParser( description='Process group(s).' )
parser.add_argument( 'groups', metavar='Group', nargs='*', help='One (or multiple) group(s) name')
parser.add_argument( '--download', action='store_true', help='Download source' )
parser.add_argument( '--suffix', help='Set suffix of output folder', required=True )
args = parser.parse_args()

output_name = '_output-{}'.format( args.suffix )
os.makedirs( output_name, exist_ok=True )

if args.download:
	data = '_data'
	os.makedirs( data, exist_ok=True )
	dst = '{}/img'.format( output_name )
	os.makedirs( dst, exist_ok=True )

for key, company_group in company_groups.items():
	if args.groups and not key in args.groups:
		continue
	
	print( 'Group: {}'.format( key ) )
	
	if args.download:
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
	with open( '{}/{}-[{}].html'.format( output_name, key, len( company_group_sorted ) ), 'w' ) as output:
		output.write( content_html )
	
	Clean( company_group )
	
	print( '' )
	
#---

if args.download:
	print( 'Write images ...' )
	for file in glob.glob( data + '/*.gif' ):
		shutil.copy( file, dst )
