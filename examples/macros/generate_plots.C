void generate_plots(void)
{
  //TFile *OldFile = TFile::Open("EffTrk2D.root");

  //auto effTrk2DCosThetaP = OldFile->Get("MarlinTrkTracks_effTrk2DCosThetaP");
  //TEfficiency *effTrk2DCosThetaP = 0;
  //OldFile->GetObject("MarlinTrkTracks_effTrk2DCosThetaP", effTrk2DCosThetaP);

  /*
  gStyle->SetNumberContours(256);
  gStyle->SetLabelFont(42,"xyz");
  gStyle->SetLabelSize(0.05,"xyz");
  gStyle->SetLabelOffset(0.015,"xyz");
  gStyle->SetTitleFont(42,"xyz");
  gStyle->SetTitleSize(0.05,"xyz");
  gStyle->SetTitleOffset(1.3,"yz");
  gStyle->SetTitleOffset(1.3,"x");
  gStyle->SetPadBottomMargin(0.28);
  gStyle->SetPadTopMargin(0.08);
  gStyle->SetPadRightMargin(0.28);
  gStyle->SetPadLeftMargin(0.27);
  */

  //effTrk2DCosThetaP->SetTitle("Tracking efficiency; cos(#theta); Momentum (GeV)");
  //effTrk2DCosThetaP->Draw("COL2Z");


  gStyle->SetNumberContours(256);
  MarlinTrkTracks_effTrk2DCosThetaP->SetTitle("Tracking efficiency; cos(#theta); Momentum (GeV)");
  MarlinTrkTracks_effTrk2DCosThetaP->Draw("COL2Z");

  MarlinTrkTracks_effTrk2DCosThetaPt->SetTitle("Tracking efficiency; cos(#theta); Pt (GeV)");
  MarlinTrkTracks_effTrk2DCosThetaPt->Draw("COL2Z");
}
