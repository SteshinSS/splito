from rdkit import Chem, DataStructs
from rdkit.Chem import AllChem
import numpy as np


def get_similar_mols(lhs_smiles, rhs_smiles, return_idx=False):
        """
        Calculated maximal similarity between two sets for each molecule.

        Parameters:
            lhs_smiles -- list of smiles
            rhs_smiles -- list of smiles
            return_idx -- if True also returns idx of the similar molecules

        Returns:
            if return_idx = False:
                nearest_sim -- list of length of lhs. i'th element contains maximal similarity between lhs[i] and rhs
            if return_idx = True:
                (nearest_sim, nearest_idx)
                nearest_idx -- list of length of lhs. i'th element contains idx of rhs molecule, which is similar to lhs[i]
        """
        lhs_mols = []
        for smiles in lhs_smiles:
            lhs_mols.append(Chem.MolFromSmiles(smiles))
        lhs_fps = [AllChem.GetMorganFingerprintAsBitVect(x, 2, 1024) for x in lhs_mols]

        rhs_mols = []
        for smiles in rhs_smiles:
            rhs_mols.append(Chem.MolFromSmiles(smiles))
        rhs_fps = [AllChem.GetMorganFingerprintAsBitVect(x, 2, 1024) for x in rhs_mols]

        nearest_sim = []
        nearest_idx = []
        for lhs in lhs_fps:
            sims = DataStructs.BulkTanimotoSimilarity(lhs, rhs_fps)
            nearest_sim.append(max(sims))
            nearest_idx.append(np.argmax(sims))
        if return_idx:
            result = (nearest_sim, nearest_idx)
        else:
            result = nearest_sim
        return result