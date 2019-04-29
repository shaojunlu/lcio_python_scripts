'''
Created on July 26, 2018

@author: S. Lu DESY
'''

from pyLCIO.drivers.Driver import Driver
from ROOT import TH1D, TH2D, TCanvas, TFile, TMath, TEfficiency
from pyLCIO import EVENT, IMPL, IOIMPL, UTIL
from math import sqrt, log10

class TrackPlotsDriver( Driver ):
    ''' TracksPlots driver to fill a histogram in an @EventLoop '''
    
    def __init__( self ):
        ''' Constructor '''
        Driver.__init__( self )
        self.histograms1D = {}
        self.histograms2D = {}
        self.efficiency1D = {}
        self.efficiency2D = {}
        self.numTracks = 0
        self.numTrk = 0
        self.mcps = [] #[] list, () tuple
        self.isGoodMCP = False
        self.bField = 3.5
        self.prefix = 'MarlinTrkTracks'
        self.rootFileNameTrackPlots = 'TrackPlots.root'
        self.hPrefix = self.prefix


    def setPrefix( self, colName ):
        ''' Set the input collection name '''
        self.hPrefix = colName
    
    def setRootFileNameTrackPlots( self, rootFileName ):
        ''' Set the output root file name '''
        self.rootFileNameTrackPlots = rootFileName
    
    def startOfData( self ):
        ''' Method called by the event loop at the beginning of the loop '''
        
        # Create histogram for filling later

        self.histograms2D[self.hPrefix+'_DenominatorCosThetaPt'] = TH2D( self.hPrefix+'_DenominatorCosThetaPt', 'Denominator;cos(#theta);pt', 40, -1., 1., 100, 0., 1. )
        self.histograms2D[self.hPrefix+'_DenominatorCosThetaP'] = TH2D( self.hPrefix+'_DenominatorCosThetaP', 'Denominator;cos(#theta);Momentum', 40, -1., 1., 100, 0., 2. )

        # TEfficiency
        self.efficiency1D[self.hPrefix+'_effTrkCosTheta'] = TEfficiency( self.hPrefix+'_effTrkCosTheta', 'Tracking efficiency;cos(#theta);efficiency', 40, -1., 1.)
        self.efficiency1D[self.hPrefix+'_effTrkPt'] = TEfficiency( self.hPrefix+'_effTrkPt', 'Tracking efficiency;Pt [GeV];efficiency', 40, -1.0, 3.0)
        self.efficiency1D[self.hPrefix+'_effTrkVtx'] = TEfficiency( self.hPrefix+'_effTrkVtx', 'Tracking efficiency; Vtx [mm];efficiency', 3000, 0., 3000.)
        self.efficiency1D[self.hPrefix+'_effTrkMom'] = TEfficiency( self.hPrefix+'_effTrkMom', 'Tracking efficiency;Momentum [GeV];efficiency', 40, -1.0, 3.0)
        self.efficiency1D[self.hPrefix+'_effTrkEnd'] = TEfficiency( self.hPrefix+'_effTrkEnd', 'effTrk vs EndPoint;End [mm];efficiency', 300, 0., 3.)
        self.efficiency2D[self.hPrefix+'_effTrk2DCosThetaPt'] = TEfficiency( self.hPrefix+'_effTrk2DCosThetaPt', 'Tracking efficiency;cos(#theta);Pt [GeV]', 40, -1., 1., 100, 0., 1.)
        self.efficiency2D[self.hPrefix+'_effTrk2DCosThetaP'] = TEfficiency( self.hPrefix+'_effTrk2DCosThetaP', 'Tracking efficiency;cos(#theta);Momentum [GeV]', 40, -1., 1., 100, 0., 2.)

        # fake rate
        self.efficiency1D[self.hPrefix+'_fakeTrkCosTheta1'] = TEfficiency( self.hPrefix+'_fakeTrkCosTheta1', 'Tracking fake rate;fake cos(#theta);fake rate', 40, -1., 1.)
        self.efficiency1D[self.hPrefix+'_fakeTrkCosTheta2'] = TEfficiency( self.hPrefix+'_fakeTrkCosTheta2', 'Tracking fake rate;fake cos(#theta);fake rate', 40, -1., 1.)
        self.efficiency1D[self.hPrefix+'_fakeTrkPt'] = TEfficiency( self.hPrefix+'_fakeTrkPt', 'Tracking fake rate;fake log(Pt) [log(GeV)];fake rate', 40, -1.0, 3.0)
        self.histograms1D[self.hPrefix+'_fakeTrkNmcp1'] = TH1D( self.hPrefix+'_fakeTrkNmcp1', 'Fake tracks;Number of MCP [/track];Entries', 20, 0.0, 10.)
        self.histograms1D[self.hPrefix+'_fakeTrkNmcp2'] = TH1D( self.hPrefix+'_fakeTrkNmcp2', 'Fake tracks;Number of MCP [/track];Entries', 20, 0.0, 10.)

        # duplicate
        self.efficiency1D[self.hPrefix+'_dupTrkCosTheta'] = TEfficiency( self.hPrefix+'_dupTrkCosTheta', 'Tracking duplicate;cos(#theta);duplicate', 40, -1., 1.)
        self.efficiency1D[self.hPrefix+'_dupTrkPt'] = TEfficiency( self.hPrefix+'_dupTrkPt', 'Tracking duplicate;Pt [GeV];duplicate', 40, -1.0, 3.0)
        self.efficiency1D[self.hPrefix+'_dupTrkVtx'] = TEfficiency( self.hPrefix+'_dupTrkVtx', 'Tracking duplicate; Vtx [mm];duplicate', 3000, 0., 3000.)
        self.efficiency1D[self.hPrefix+'_dupTrkMom'] = TEfficiency( self.hPrefix+'_dupTrkMom', 'Tracking duplicate;Momentum [GeV];duplicate', 40, -1.0, 3.0)
        self.efficiency1D[self.hPrefix+'_dupTrkEnd'] = TEfficiency( self.hPrefix+'_dupTrkEnd', 'Tracking duplicate;End [mm];duplicate', 300, 0., 3.)

    
    def processEvent( self, event ):
        ''' Method called by the event loop for each event '''
        self.numTrk = 0
        self.numTracks = 0

        del self.mcps[:]

        # Get generator particle information
        McP = event.getCollection( "MCParticle" )
        for p in McP :
            if abs( p.getCharge()) < 0.5 :
                continue

            # get information fo charge particle
            mcpCosTheta = p.getMomentum()[2] / sqrt( p.getMomentum()[0] * p.getMomentum()[0] + p.getMomentum()[1] * p.getMomentum()[1] + p.getMomentum()[2] * p.getMomentum()[2] )
            mcpMom = sqrt( p.getMomentum()[0] * p.getMomentum()[0] + p.getMomentum()[1] * p.getMomentum()[1] + p.getMomentum()[2] * p.getMomentum()[2] )
            mcpPt = sqrt( p.getMomentum()[0] * p.getMomentum()[0] + p.getMomentum()[1] * p.getMomentum()[1] )
            mcpVtx = sqrt( p.getVertex()[0] * p.getVertex()[0] + p.getVertex()[1] * p.getVertex()[1] + p.getVertex()[2] * p.getVertex()[2] )
            mcpEnd = sqrt( p.getEndpoint()[0] * p.getEndpoint()[0] + p.getEndpoint()[1] * p.getEndpoint()[1] + p.getEndpoint()[2] * p.getEndpoint()[2] )
            mcpEndRho = sqrt( p.getEndpoint()[0] * p.getEndpoint()[0] + p.getEndpoint()[1] * p.getEndpoint()[1] )

            # Particle should not be decayed in Tracker.
            #if p.isDecayedInTracker() == True : #False: #True :
            #    continue

            #if mcpPt < 0.100 : #0.1GeV = 100MeV 
            #    continue

            # Particle should not go into beam pipe
            if abs( mcpCosTheta ) > 0.99 :
                continue

            # Particle is not from overlay
            if p.isOverlay() == True :
                continue

            if p.getGeneratorStatus() == 1 and mcpVtx < 100.0 :
                self.mcps.append(p)
                self.isGoodMCP = True


        # Get Track information
        isTrkFound = False
        isDupTrk = False
        # Get the MCTruthMarlinTrkTracksLink collection from the event
        mcpToTrk = event.getCollection( "MCTruthMarlinTrkTracksLink" )
        navMcptTrk = UTIL.LCRelationNavigator( mcpToTrk )
        TrkToMcp = event.getCollection( "MarlinTrkTracksMCTruthLink" )
        navTrktMcp = UTIL.LCRelationNavigator( TrkToMcp )
        for mu in self.mcps:
            mcpCosTheta = mu.getMomentum()[2] / sqrt( mu.getMomentum()[0] * mu.getMomentum()[0] + mu.getMomentum()[1] * mu.getMomentum()[1] + mu.getMomentum()[2] * mu.getMomentum()[2] )
            mcpMom = sqrt( mu.getMomentum()[0] * mu.getMomentum()[0] + mu.getMomentum()[1] * mu.getMomentum()[1] + mu.getMomentum()[2] * mu.getMomentum()[2] )
            mcpPt = sqrt( mu.getMomentum()[0] * mu.getMomentum()[0] + mu.getMomentum()[1] * mu.getMomentum()[1] )
            mcpVtx = sqrt( mu.getVertex()[0] * mu.getVertex()[0] + mu.getVertex()[1] * mu.getVertex()[1] + mu.getVertex()[2] * mu.getVertex()[2] )

            # tracks include this mcp
            trks = navMcptTrk.getRelatedToObjects( mu )
            # percent of track hits made of this mcp 
            testFromWgt = navTrktMcp.getRelatedFromWeights( mu )

            # percent of mcp hits contribute to a track
            #testFromWgt4 = navMcptTrk.getRelatedToWeights( mu )


            SimTrkVTX = event.getCollection( "VXDCollection" )
            Nvtx = 0
            for vtx in SimTrkVTX:
                if vtx.getMCParticle() == mu :
                    Nvtx = Nvtx + 1
                    if Nvtx > 3 :
                        break

            SimTrkSIT = event.getCollection( "SITCollection" )
            Nsit = 0
            for sit in SimTrkSIT:
                if sit.getMCParticle() == mu :
                    Nsit = Nsit + 1 
                    if Nsit > 3 :
                        break

            #if mcpCosTheta < 0.9 and ( Nvtx + Nsit ) < 4 :
            #    continue

            SimTrkFTD = event.getCollection( "FTDCollection" )
            Nftd = 0
            for ftd in SimTrkFTD:
                if ftd.getMCParticle() == mu :
                    Nftd = Nftd + 1 
                    if Nftd > 3 :
                        break

            #if mcpCosTheta >= 0.9 and ( Nftd + Nsit ) < 4 :
            #    continue

            if ( Nvtx + Nsit + Nftd) < 4 :
                continue


            iTrk = 0
            iDupTrk = 0
            for tr in trks :
                if testFromWgt[iTrk] > 0.75 :
                    isTrkFound = True
                    iDupTrk = iDupTrk + 1
                iTrk = iTrk+1

            self.efficiency1D[self.hPrefix+'_effTrkCosTheta'].Fill(isTrkFound, mcpCosTheta)
            self.efficiency1D[self.hPrefix+'_effTrkPt'].Fill(isTrkFound, log10(mcpPt))
            self.efficiency1D[self.hPrefix+'_effTrkMom'].Fill(isTrkFound, log10(mcpMom))
            self.efficiency1D[self.hPrefix+'_effTrkVtx'].Fill(isTrkFound, mcpVtx)
            self.efficiency1D[self.hPrefix+'_effTrkEnd'].Fill(isTrkFound, log10(mcpEnd))
            self.efficiency2D[self.hPrefix+'_effTrk2DCosThetaPt'].Fill(isTrkFound, mcpCosTheta, mcpPt)
            self.efficiency2D[self.hPrefix+'_effTrk2DCosThetaP'].Fill(isTrkFound, mcpCosTheta, mcpMom)
            self.histograms2D[self.hPrefix+'_DenominatorCosThetaPt'].Fill(mcpCosTheta,mcpPt)
            self.histograms2D[self.hPrefix+'_DenominatorCosThetaP'].Fill(mcpCosTheta,mcpMom)


            if iDupTrk > 1 :
                isDupTrk = True
                iDupTrk = 0

            self.efficiency1D[self.hPrefix+'_dupTrkCosTheta'].Fill(isDupTrk, mcpCosTheta)
            self.efficiency1D[self.hPrefix+'_dupTrkPt'].Fill(isDupTrk, log10(mcpPt))
            self.efficiency1D[self.hPrefix+'_dupTrkMom'].Fill(isDupTrk, log10(mcpMom))
            self.efficiency1D[self.hPrefix+'_dupTrkVtx'].Fill(isDupTrk, mcpVtx)
            self.efficiency1D[self.hPrefix+'_dupTrkEnd'].Fill(isDupTrk, log10(mcpEnd))

            isTrkFound = False
            isDupTrk = False


        MTrks = event.getCollection( "MarlinTrkTracks" )
            
        recoPt = 0.0
        recCosth = 0.0

        isFakeTrk = True

        for tr in MTrks :
            d0mcp = tr.getD0()
            #phmcp = tr.getPhi0()
            ommcp = tr.getOmega()
            #z0mcp = tr.getZ0()
            tLmcp = tr.getTanLambda()

            recoPt = abs(((3.0/10000.0)*3.5)/ommcp)
            recCosth = tLmcp/sqrt(1.0+tLmcp*tLmcp)

            MCPsTrk = navTrktMcp.getRelatedToObjects( tr )
            testToWgt = navTrktMcp.getRelatedToWeights( tr )
            for iTs in testToWgt :
                if iTs >= 0.75 :      # group of hits >= 75% from one MCP, consided as real reco track for this MCP, 
                    isFakeTrk = False # is not fake reco track.

            self.efficiency1D[self.hPrefix+'_fakeTrkCosTheta1'].Fill(isFakeTrk, recCosth)
            self.efficiency1D[self.hPrefix+'_fakeTrkPt'].Fill(isFakeTrk, log10(recoPt))

            if isFakeTrk == True : # check the fake track: Number of MCP
                self.histograms1D[self.hPrefix+'_fakeTrkNmcp1'].Fill(MCPsTrk.size())

            if MCPsTrk.size() == 2:
                Daus0 =  MCPsTrk[0].getDaughters()
                for da0 in Daus0:
                    if da0 == MCPsTrk[1]:
                        isFakeTrk = False
                        #print("Pa0: ",MCPsTrk[0].getPDG()," Da1: ", MCPsTrk[1].getPDG())
                Daus1 =  MCPsTrk[1].getDaughters()
                for da1 in Daus1:
                    if da1 == MCPsTrk[0]:
                        isFakeTrk = False
                        #print("Pa1: ",MCPsTrk[1].getPDG()," Da0: ", MCPsTrk[0].getPDG())

            if isFakeTrk == True : # check the fake track: Number of MCP
                self.histograms1D[self.hPrefix+'_fakeTrkNmcp2'].Fill(MCPsTrk.size())

            self.efficiency1D[self.hPrefix+'_fakeTrkCosTheta2'].Fill(isFakeTrk, recCosth)

            isFakeTrk = True



    def endOfData( self ):
        ''' Method called by the event loop at the end of the loop '''

        # Create a root file, and write out histograms
        myfile = TFile( self.rootFileNameTrackPlots, 'RECREATE' )


        for hName in self.histograms1D:
            self.histograms1D[hName].Write()

        for hName in self.histograms2D:
            self.histograms2D[hName].Write()

        for hName in self.efficiency1D:
            self.efficiency1D[hName].Write()

        for h2DName in self.efficiency2D:
            self.efficiency2D[h2DName].Write()

        myfile.Close()
        
        #userInput = raw_input( 'Press any key to continue' )
