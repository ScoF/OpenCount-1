"""
An abstract base class to be used for vendor-specific functions, such
as barcode decoding.
"""

class Vendor(object):
    def __init__(self, proj):
        pass
        #raise NotImplementedError("Can't instantiate abstract Vendor class.")

    def decode_ballots(self, ballots, *args, **kwargs):
        """
        Use automated image-processing algorithms to output an initial
        decoding for each voted ballot. The user will then verify the
        output using overlay-verification.

        Input:
            dict BALLOTS: {int ballotID: [imgpath_side0, ...]}.
        Output:
            (dict FLIP_MAP,
             dict VERIFYPATCH_BBS,
             list ERR_IMGPATHS)

        FLIP_MAP: stores whether an image is flipped or not:
            {str imgpath: bool isFlipped}
        VERIFYPATCHES_BBS: stores the locations of barcode patches that
            need to be verified by the user:
                {str bc_val: [(str imgpath, (x1,y1,x2,y2), userinfo), ...]}
            For instance, the keys to this dict could be '0' and '1'
            for Sequoia, Diebold, and ES&S (indicating whitespace and
            and timing marks respectively). USERINFO can be any additional
            information that your decoder needs (for example, an integer
            ID that records which digit this encodes).
        ERR_IMGPATHS: List of voted imgpaths that were unable to be 
            successfully decoded. These will be handled specially.
        """
        raise NotImplementedError("Implement your own decode_ballots.")

    def partition_ballots(self, verified_results, manual_labeled):
        """
        Given the user-verified (and corrected) results of decode_ballots,
        output the partitioning.

        Input:
            dict VERIFIED_RESULTS: {str bc_val: [(str imgpath, (x1,y1,x2,y2), userinfo), ...]}
            dict MANUAL_LABELED: {str imgpath: str label}
        Output:
            (dict PARTITIONS, 
             dict IMG2DECODING,
             dict IMAGE_INFO)

        PARTITIONS: stores the partitioning as:
            {int partitionID: [int ballotID_i, ...]}
        IMG2DECODING: stores barcode strings for each image as:
            {str imgpath: [str bc_i, ...]}
        IMAGE_INFO: stores meaningful info for each image:
                {str imgpath: {str PROPNAME: str PROPVAL}}
            where PROPNAME could be 'page', 'party', 'precinct', etc.
            The key 'page' must be present. 'page' should
            map to an integer, i.e. 0,1 is 'Front', 'Back' respectively.
        """
        raise NotImplementedError("Implement your own partition_ballots.")

    def split_contest_to_targets(self, ballot_image, contest, targets):
        """
        Given an image of a contest, extract 
            (a) the tile and 
            (b) each of the voting targets
        
        Input:
            PIL Image: ballot_image
            (int left, int up, int right, int down) contest
            targets: [(int left, int up, int right, int down),...]
        
        Output:
            [(int upper, int lower),...], the upper and lower coords of each thing to extract
        """
        
        l,u,r,d = contest
        tops = sorted([a[1]-u-10 for a in targets])+[d]
        if tops[0] > 0:
            tops = [0]+tops
        else:
            tops = [0,0]+tops[1:] # In case the top is negative.

        blocks = []
        for upper,lower in enumerate(zip(tops, tops[1:])):
            blocks.append((upper, lower))
        
        return blocks
        
        

    def __repr__(self):
        return 'Vendor()'
    def __str__(self):
        return 'Vendor()'
